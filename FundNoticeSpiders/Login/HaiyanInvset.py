# -*- coding: utf-8 -*-

import config
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider
from pyquery import PyQuery
import re


class HaiyanInvsetSpider(GGFundNoticeSpider):
    name = 'FundNotice_HaiyanInvset'
    sitename = '海燕投资'
    channel = '公告'
    entry = 'http://www.haiyancap.com/pc/profit/all'
    allowed_domains = ['www.haiyancap.com']

    proxy = config.proxy
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(HaiyanInvsetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.haiyancap.com/pc/login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        authenticity_token = response.xpath(".//input[@name='authenticity_token']/@value").extract_first()
        yield FormRequest(url='http://www.haiyancap.com/pc/login/submit_user',
                          formdata={'login_name': '13916427906',
                                    'password': 'ZYYXSM123',
                                    'utf8': '✓',
                                    'authenticity_token': authenticity_token,
                                    'auto_login': 'on',
                                    'login': '0',
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield Request(url='http://www.haiyancap.com/pc/profit/all',
                      meta={
                          'ref': 'http://www.haiyancap.com/pc/profit/index'},
                      callback=self.parse_pre_list
                      )

    def parse_pre_list(self, response):
        fund_ids = response.css(r'tbody.tbody_w>tr>td:last-child>div:nth-child(2)>a::attr(href)').re(
            r'/mobile/appointment/(\S+)/consult')
        for fund_id in fund_ids:
            self.lps.append({
                'url': 'http://www.haiyancap.com/pc/products/1/show_data/0/show/' + fund_id,
                'ref': response.url,
                'ext': {'fund_id': fund_id}
            })
        yield self.request_next()

    def parse_list(self, response):
        ext = response.meta['ext']
        fund_id = ext['fund_id']
        csrf_token = response.css('html head meta[name="csrf-token"]::attr(content)').extract_first()

        self.ips.append({
            'url': 'http://www.haiyancap.com/pc/products/' + fund_id + '/report',
            'headers': {
                'X-CSRF-Token': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
                'Pragma': 'no-cache',
            },
            'ref': 'http://www.haiyancap.com/pc/products/1/show_data/0/show/' + fund_id,
        })

        yield self.request_next()

    def parse_item(self, response):
        html_str = response.text.replace('$("#pagination").detach();', '').replace('$("#content").append(', '').replace(
            '$("#content").html("");', '').replace('$("#content").after(', '').replace(');', '').replace('\\', '').replace('\n\r\t', '')
        html = PyQuery(html_str)
        for a in html.items('a[target="_blank"]'):
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            url = a.attr('href')
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = a('p:first-child').text().replace('.pdf', '').replace('.docx', '').replace('.doc', '')
            publish_time = a('p:nth-child(2)').text()
            publish_time = re.search('\d+-\d+-\d+', publish_time).group(0)
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
        url = html('div>nav>span>a[rel="next"]').attr('href')
        if url is not None:
            self.ips.insert(0, {
                'url': urljoin(get_base_url(response), url),
                'headers': response.request.headers,
                'ref': response.request.headers['Referer']
            })
        yield self.request_next()
