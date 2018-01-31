# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SZqhhqzbSpider(GGFundNavSpider):
    name = 'FundNav_SZqhhqzb'
    sitename = '深圳前海慧泉基金'
    channel = '投资顾问'
    allowed_domains = ['www.hqzb-china.com']

    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(SZqhhqzbSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.hqzb-china.com', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.hqzb-china.com/member.php?a=login',
                          formdata={'name': 'ZYYXSM',
                                    'pwd': 'ZYYXSM123',
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):

        yield Request(url='http://www.hqzb-china.com/product.php', callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        fps = []
        ips = []

        urls = response.xpath("//div[@class='NY_left']/ul/li/a/@href").extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            fps.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//div[@class='NY_Product_sort']/ul/li/a/@href").extract()
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
        fund_name = response.xpath("//div[@class='NY_Product_sort']/ul/li/a/text()").extract_first()
        rows = response.css('table>tbody>tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = fund_name

            statistic_date = row.css('td:first-child').re_first(r'\d+-\d+-\s*\d+')
            item['statistic_date'] = datetime.strptime(statistic_date.replace(' ', ''), '%Y-%m-%d')

            nav = row.css('td:nth-child(2)').re_first(r'>\s*?([0-9.]+)\s*?<')
            item['nav'] = float(nav) if nav else None

            yield item

        yield self.request_next(fps, ips)
