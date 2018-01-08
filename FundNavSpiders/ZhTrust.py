# -*- coding: utf-8 -*-

import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ZhTrustSpider(GGFundNavSpider):
    name = 'FundNav_ZhTrust'
    sitename = '中海信托'
    channel = '信托净值'
    allowed_domains = ['www.zhtrust.com']
    start_urls = ['http://www.zhtrust.com/product/']

    def __init__(self, limit=None, *args, **kwargs):
        super(ZhTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.zhtrust.com/product/index.shtml', callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://www.zhtrust.com/front/fund/Product/findProductBySearch.do?gotoPage=' + str(
                    pg),
                'ref': response.url,
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('.down>.pan>h4>a').xpath(r'self::a[re:test(@href, ".+?fundcode=\d+")]')
        for fund in funds:
            url = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
            code = fund.css('::attr(href)').re_first(r'.+fundcode=(\d+)')
            ips.append({
                'url': 'http://www.zhtrust.com/front/fund/Product/findProductNetByFundCode.do',
                'form': {'fundcode': code, 'beginDate': '', 'endDate': ''},
                'ref': url
            })

        n = response.css('.yue>.page a#next').xpath(r'self::a[re:test(text(), "\s*下一页\s*")]').xpath(
            r'self::a[re:test(@href, "javascript:loadQaPage\(\d+\);")]')
        if n is not None and n:
            pg = n.css('::attr(href)').re_first(r'javascript:loadQaPage\((\d+)\);')
            fps.append({
                'pg': int(pg),
                'url': response.meta['url'],
                'ref': response.request.headers['Referer']
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = json.loads(response.text)
        if rows is not None:
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.request.headers['Referer']

                item['fund_name'] = row['pro_name']

                statistic_date = row['net_date']
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

                nav = row['unit_net']
                item['nav'] = float(nav) if nav is not None else None

                added_nav = row['total_net']
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item

        yield self.request_next(fps, ips)
