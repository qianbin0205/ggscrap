# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SanlueSpider(GGFundNavSpider):
    name = 'FundNav_Sanlue'
    sitename = '前海三略资产'
    channel = '投顾净值'
    allowed_domains = ['www.san-lue.com']
    start_urls = ['http://www.san-lue.com/']

    def __init__(self, limit=None, *args, **kwargs):
        super(SanlueSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.san-lue.com/zgrd?id=1', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.san-lue.com/user/checklogin',
                          formdata={'backtourl': '/index',
                                    'username': 'ZYYXSM',
                                    'password': 'ZYYXSM123'},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.san-lue.com/pro/1/1',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('.jijinxx_body>.gscp_b_left>ul>li a').xpath(r'self::a[re:test(@href, "/pro/\d+/1")]')
        for fund in funds:
            fund_name = fund.css('::text').extract_first()
            url = fund.css('::attr(href)').re_first(r'(/pro/\d+/)1')
            url = urljoin(get_base_url(response), url + '2')
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name},
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = response.xpath("//div[@class='gscp_br_lsyj']/table/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = fund_name

            statistic_date = row.xpath(".//td[1]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath("./td[3]/text()").extract_first()
            item['nav'] = float(nav)

            added_nav = row.xpath("./td[4]/text()").extract_first()
            item['added_nav'] = float(added_nav)

            yield item
        url = response.xpath("//a[text()='下一页']/@href").extract_first()
        url = urljoin(get_base_url(response), url)
        if url != response.url:
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': ext,
            })

        yield self.request_next(fps, ips)