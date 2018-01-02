# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SzhvcSpider(GGFundNavSpider):
    name = 'FundNav_Szhvc'
    sitename = '丰岭资本'
    channel = '投顾净值'
    allowed_domains = ['www.szhvc.com']
    start_urls = ['http://www.szhvc.com/memberCenter/recommend']

    def __init__(self, limit=None, *args, **kwargs):
        super(SzhvcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://www.szhvc.com/api/pc/product/list?pageNum=' + str(pg),
                'ref': 'http://www.szhvc.com/memberCenter/recommend',
                'username': '18602199319',
                'passowrd': 'yadan0319',
                'cookies': 'td_cookie=11049207; td_cookie=11049224; SESSIONID=b67c14de-5627-40be-a32e-950086a4cca2; userinfo=s%3ALEjGVc7P6Ale8ydZWaIB6WRiXjwI_EIp.45uSNrSO0%2BA7Hn69FDrNwsWF8bEfxGwzXKXBsjdY%2FbQ'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        resp = json.loads(response.text)
        funds = resp['collection']
        for fund in funds:
            ips.append({
                'pg': 1,
                'url': lambda pg: 'http://www.szhvc.com/api/pc/product/' + str(
                    fund['productId']) + '/netValues?pageNum=' + str(pg),
                'ref': 'http://www.szhvc.com/memberCenter/recommend?productDetails=' + str(fund['productId']),
                'ext': {'fund_name': fund['productShortName']}
            })

        pages = resp['property']['pages']
        page = response.meta['pg']
        url = response.meta['url']
        if page < pages:
            fps.append({
                'pg': page + 1,
                'url': url,
                'ref': response.request.headers['Referer']
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        ext = response.meta['ext']
        fund_name = ext['fund_name']

        resp = json.loads(response.text)
        rows = resp['collection']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = fund_name

            statistic_date = row['netDate']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row['netValue']
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row['accumulatedNet']
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item

        pages = resp['property']['pages']
        page = response.meta['pg']
        url = response.meta['url']
        if page < pages:
            ips.append({
                'pg': page + 1,
                'url': url,
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
