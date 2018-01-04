# -*- coding: utf-8 -*-

import json
from datetime import datetime
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
        cookies = 'td_cookie=11049207; td_cookie=11049224; SESSIONID=48b1f78d-6265-4c58-b1a7-a5ecf557345f; userinfo=s%3AkMxNBcQcpDuFOn3HQKAWTNoUsMl-ChBc.NvR5QCH%2B%2BSMgBUxDFsYwhKxZo4qWMsFySoh9Bop7PBw'
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://www.szhvc.com/api/pc/product/list?pageNum=' + str(pg),
                'ref': 'http://www.szhvc.com/memberCenter/recommend',
                'username': '18602199319',
                'passowrd': 'yadan0319',
                'cookies': cookies
            }
        ]

        # product_id = 276
        # product_name = '丰岭稳健成长6期证券投资基金'
        # ips = [
        #     {
        #         'pg': 1,
        #         'url': lambda pg: 'http://www.szhvc.com/api/pc/product/' + str(
        #             product_id) + '/netValues?pageNum=' + str(
        #             pg),
        #         'ref': 'http://www.szhvc.com/memberCenter/recommend?productDetails=' + str(product_id),
        #         'ext': {'fund_name': product_name},
        #         'cookies': cookies
        #     }
        # ]
        # yield self.request_next([], ips)

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        resp = json.loads(response.text)
        funds = resp['collection']
        for fund in funds:
            ips.append({
                'pg': {'page': 1, 'pid': fund['productId']},
                'url': lambda pg: 'http://www.szhvc.com/api/pc/product/' + str(pg['pid']) + '/netValues?pageNum=' + str(
                    pg['page']),
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
        if rows is not None:
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

        if 'property' in resp:
            pages = resp['property']['pages']
            pg = response.meta['pg']
            url = response.meta['url']
            if pg['page'] < pages:
                pg['page'] += 1
                ips.append({
                    'pg': pg,
                    'url': url,
                    'ref': response.request.headers['Referer'],
                    'ext': {'fund_name': fund_name}
                })

        yield self.request_next(fps, ips)
