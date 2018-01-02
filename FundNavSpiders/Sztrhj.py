# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SztrhjSpider(GGFundNavSpider):
    name = 'FundNav_Sztrhj'
    sitename = '深圳泰润海吉资产'
    channel = '投资顾问'
    allowed_domains = ['www.sztrhj.com']
    start_urls = ['http://www.sztrhj.com/tairun/product/']

    def __init__(self, limit=None, *args, **kwargs):
        super(SztrhjSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.sztrhj.com/tairun/product/',
                'ref': None,
                'username': '13523794375',
                'password': '123456'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.css('.pro_box>table.pro_table tr>td:first-child a::attr(href)').extract()
        for u in urls:
            u = urljoin(get_base_url(response), u)
            ips.append({
                'url': u,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = response.css('table.pro_table.jz tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = row.css('td:first-child').re_first(r'>([^<>]+)<')

            statistic_date = row.css('td:nth-child(3)').re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['added_nav'] = float(row.css('td:nth-child(2)').re_first(r'>\s*?([0-9.]+)\s*?<'))
            yield item

        url = response.css('ul.pagelist>li a').xpath('self::a[re:test(text(), "\s*下一页\s*")]/@href').extract_first()
        if url is not None:
            url = urljoin(get_base_url(response), url)
            ips.insert(0, {
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)
