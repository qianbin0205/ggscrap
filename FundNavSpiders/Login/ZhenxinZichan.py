# -*- coding: utf-8 -*-

import config
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ZhenxinZichanSpider(GGFundNavSpider):
    name = 'FundNav_ZhenxinZichan'
    sitename = '北京真鑫资产'
    channel = '投资顾问'
    allowed_domains = ['www.zhenxinzichan.com']

    proxy = config.proxy

    start_urls = []
    fps = [
        {
            'url': 'http://www.zhenxinzichan.com/pc/profit/all',
            'ref': 'http://www.zhenxinzichan.com/pc/profit/all',
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(ZhenxinZichanSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.zhenxinzichan.com/pc/login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        authenticity_token = response.xpath(".//input[@name='authenticity_token']/@value").extract_first()
        yield FormRequest(url='http://www.zhenxinzichan.com/pc/login/submit_user',
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
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.css(r'#products>.w_a_xi01.bg_xi>a::attr(href)').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        fund_name = response.xpath("//div[@class='top_title_01']/text()").extract_first()
        rows = response.xpath("//div[@id='nets']/table/tbody/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[1]/text()").re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath("./td[2]").re_first(r'>\s*([0-9.]+)\s*<')
            item['nav'] = float(nav) if nav else None

            added_nav = row.xpath("./td[3]").re_first(r'>\s*([0-9.]+)\s*<')
            item['added_nav'] = float(added_nav) if added_nav else None

            yield item

        yield self.request_next(fps, ips)
