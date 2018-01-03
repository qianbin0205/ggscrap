# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class JroyalSpider(GGFundNavSpider):
    name = 'FundNav_Jroyal'
    sitename = '珺容投资'
    channel = '投顾净值'
    allowed_domains = ['www.jroyal.cn']
    start_urls = ['http://www.jroyal.cn/product_pid_22.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(JroyalSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.jroyal.cn/default.ashx?xmls=xmls/user.xmls&method=login',
                          formdata={'Idnumber': '410333198909180214',
                                    'Password': '123456',
                                    'PasswordRecord': '1',
                                    'goto': ''},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.jroyal.cn/product_pid_22.html',
                'ref': None,
            }
        ]

        # url = 'http://www.jroyal.cn/product_cid_124_pid_23.html'
        # yield self.request_next([], [{'url': url, 'ref': None}])

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('.fund_side ul.bbbb>li>a')
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

        rows = response.css('#cataproduct.fund-table tbody tr')
        if rows.css('td:nth-child(4)').extract_first() is not None:
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url

                item['fund_name'] = row.css('td:first-child').re_first(r'>([^<>]+)<')

                statistic_date = row.css('td:nth-child(2)').re_first(r'\d+-\d+-\d+')
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                item['nav'] = float(row.css('td:nth-child(3)').re_first(r'>\s*?([0-9.]+)\s*?<'))
                item['added_nav'] = float(row.css('td:nth-child(4)').re_first(r'>\s*?([0-9.]+)\s*?<'))
                yield item

        url = response.css('#pages>ul>li a').xpath('self::a[re:test(text(), "\s*下一页\s*")]/@href').extract_first()
        if url is not None and url is not '#':
            url = urljoin(get_base_url(response), url)
            ips.insert(0, {
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)
