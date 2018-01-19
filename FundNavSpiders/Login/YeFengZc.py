# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class YeFengZcSpider(GGFundNavSpider):
    name = 'FundNav_YeFengZc'
    sitename = '野风资产'
    channel = '投顾净值'
    allowed_domains = ['www.yefengzc.com']
    start_urls = ['http://www.yefengzc.com/qxcp']

    def __init__(self, limit=None, *args, **kwargs):
        super(YeFengZcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.yefengzc.com/userlogin?returnurl=',
                          formdata={'Username': '820612602@qq.com',
                                    'Password': '123456'},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.yefengzc.com/qxcp',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('.w_vnav_item>h3>a').xpath('self::a[re:test(text(), "\s*>[^<>]+\s*")]')

        for fund in funds:
            url = fund.css('::attr(href)').extract_first()
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = response.css('.editableContent tr.firstRow').xpath('following-sibling::tr')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            ls = row.css('td:first-child').css('::text').extract()
            fund_name = ''.join(ls)
            item['fund_name'] = fund_name

            ls = row.css('td:nth-child(2)').css('::text').extract()
            statistic_date = ''.join(ls)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            ls = row.css('td:nth-child(3)').css('::text').extract()
            nav = ''.join(ls)
            item['nav'] = float(nav)

            yield item

        yield self.request_next(fps, ips)
