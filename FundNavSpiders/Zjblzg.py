# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ZjblzgSpider(GGFundNavSpider):
    name = 'FundNav_Zjblzg'
    sitename = '白鹭资管'
    channel = '投资顾问'
    allowed_domains = ['www.zjblzg.com']
    start_urls = ['http://www.zjblzg.com/value']

    def __init__(self, limit=None, *args, **kwargs):
        super(ZjblzgSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        ips = [
            {
                'pg': 1,
                'url': 'http://www.zjblzg.com/front/getValueInfo',
                'form': {'pageNo': lambda pg: str(pg)},
                'ref': 'http://www.zjblzg.com/value',
                'username': '13083790899',
                'password': '123456',
                'cookies': 'JSESSIONID=5D93FC091E7CDAFF3D47F7029CC0003A; td_cookie=11049235'
            }
        ]

        yield self.request_next([], ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        # pg = response.meta['pg']
        url = response.meta['url']
        form = response.meta['form']
        ips.append({
            'pg': 2,
            'url': url,
            'form': form,
            'ref': response.request.headers['Referer']
        })

        rows = json.loads(response.text)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = row['name']

            statistic_date = row['value_time']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d %H:%M:%S')

            nav = row['new_value']
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row['week']
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item

        yield self.request_next(fps, ips)
