# -*- coding: utf-8 -*-

from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import json


class AnXinzqSpider(GGFundNavSpider):
    name = 'FundNav_AnXinzq'
    sitename = '安信证券'
    channel = '券商资管净值'
    allowed_domains = ['mall.essence.com.cn']
    start_urls = ['https://mall.essence.com.cn/mall/views/financial/zigIndex.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(AnXinzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'pg': 1,
                'url': 'https://mall.essence.com.cn/servlet/json',
                'form': {'funcNo': '1000050', 'product_shelf': '1', 'fina_belongs': '1', 'page': lambda pg: str(pg),
                         'numPerPage': '500', 'risk_level': '', 'profit_type': '', 'product_expires_start': '',
                         'product_expires_end': '',
                         'fina_type': '0', 'per_buy_limit_start': '', 'per_buy_limit_end': '', 'search_value': '',
                         'user_id': '', 'asset_busin_type': ''},
                'ref': 'https://mall.essence.com.cn/mall/views/financial/zigIndex.html',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        url = response.meta['url']
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = response.meta['pg']
        form = response.meta['form']

        totalpage = json.loads(response.text)['results'][0]['totalPages']
        if pg < totalpage:
            fps.append({
                'pg': pg + 1,
                'url': url,
                'form': form,
                'ref': response.request.headers['Referer']
            })

        funds = json.loads(response.text)['results'][0]['data']
        for fund in funds:
            fund_name = fund['product_abbr']
            fund_code = fund['product_code']
            ips.append({
                'pg': 1,
                'url': 'https://mall.essence.com.cn/servlet/json',
                'form': {'funcNo': '1000055', 'product_code': fund_code, 'page': lambda pg: str(pg),
                         'numPerPage': '500',
                         'start_date': '', 'end_date': '', 'fund_type': '0'},
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        pg = response.meta['pg']
        url = response.meta['url']
        fund_name = ext['fund_name']
        rows = json.loads(response.text)['results'][0]['data']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = fund_name

            statistic_date = row['nav_date']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row['nav']
            item['nav'] = float(nav)

            added_nav = row['cumulative_net']
            item['added_nav'] = float(added_nav)

            yield item
        form = response.meta['form']
        totalpages = json.loads(response.text)['results'][0]['totalPages']
        if pg < totalpages:
            ips.insert(0, {
                'pg': pg + 1,
                'url': url,
                'form': form,
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
