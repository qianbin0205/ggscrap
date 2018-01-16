# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class GZDaShuSpider(GGFundNavSpider):
    name = 'FundNav_GZDaShu'
    sitename = '广州大树投资'
    channel = '投资顾问'
    allowed_domains = ['www.gzdashu.com']
    start_urls = ['http://www.gzdashu.com/cpzx.aspx']

    def __init__(self, limit=None, *args, **kwargs):
        super(GZDaShuSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.gzdashu.com/login.aspx',
                          formdata={'returnUrl': '/',
                                    'username': '18638357950',
                                    'password': '123456',
                                    'rememberMe': 'true'},
                          meta={
                              'handle_httpstatus_list': [302]
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.gzdashu.com/cpzx.aspx',
                'ref': 'http://www.gzdashu.com/',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath(r'//a[re:test(@id, "^qxcp[0-9]+$")]')
        for fund in funds:
            url = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = response.css('table.mychat tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            fund_name = row.css('td:nth-child(1)::text').extract_first()
            item['fund_name'] = fund_name

            statistic_date = row.css('td:nth-child(4)::text').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

            if fund_name == '择时对冲一号':
                item['nav_2'] = float(row.css('td:nth-child(2)::text').extract_first())
                item['added_nav_2'] = float(row.css('td:nth-child(3)::text').extract_first())
            else:
                item['nav'] = float(row.css('td:nth-child(2)::text').extract_first())
                item['added_nav'] = float(row.css('td:nth-child(3)::text').extract_first())

            yield item

        yield self.request_next(fps, ips)
