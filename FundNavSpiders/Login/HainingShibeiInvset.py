# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class HainingShibeiInvsetSpider(GGFundNavSpider):
    name = 'FundNav_HainingShibeiInvset'
    sitename = '海宁拾贝投资'
    channel = '投顾净值'
    allowed_domains = ['www.tbamc.com']

    start_urls = []
    fps = [
        {
            'url': 'http://www.tbamc.com/pc/profit/all',
            'ref': 'http://www.tbamc.com/pc/profit/index',
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(HainingShibeiInvsetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.tbamc.com/pc/login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        authenticity_token = response.xpath(".//input[@name='authenticity_token']/@value").extract_first()
        yield FormRequest(url='http://www.tbamc.com/pc/login/submit_user',
                          formdata={'login_name': '17839170174',
                                    'password': '123456',
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
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css(r'tbody.tbody_w>tr>td:first-child>a::attr(href)').extract()
        for fund in funds:
            u = fund.rsplit('/', 1)[1]
            ips.append({
                'url': 'http://www.tbamc.com/pc/products/0/show_data/0/show/' + u,
                'ref': response.url
            })

        url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if url is not None:
            url = urljoin(get_base_url(response), url)
            fps.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        fund_name = response.xpath("//div[@class='line_bg_left']/p/text()").extract_first()
        rows = response.xpath("//div[@id='nets']/table/tbody/tr")
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[1]/text()").re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.xpath("./td[2]/text()").extract_first())
            item['added_nav'] = float(row.xpath("./td[3]/text()").extract_first())

            yield item

        yield self.request_next(fps, ips)
