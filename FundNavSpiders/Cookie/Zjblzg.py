# -*- coding: utf-8 -*-

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

    username = '13083790899'
    password = '123456'
    cookies = 'td_cookie=11049086; JSESSIONID=097AF9795804B74603B125A78B190653'

    def __init__(self, limit=None, *args, **kwargs):
        super(ZjblzgSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.zjblzg.com/value',
                'ref': 'http://www.zjblzg.com/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        statistic_date = response.css('p').re_first(r'白鹭产品每周净值\((\d+)\)')
        statistic_date = datetime.strptime(statistic_date, '%Y%m%d')

        for i in range(1, 3):
            ips.append({
                'pg': i,
                'url': 'http://www.zjblzg.com/front/getValueInfo',
                'form': {'pageNo': lambda pg: str(pg)},
                'ref': response.url,
                'ext': {'statistic_date': statistic_date}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        rows = json.loads(response.text)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = row['name']

            # statistic_date = row['value_time']
            # item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d %H:%M:%S')
            item['statistic_date'] = ext['statistic_date']

            nav = row['new_value']
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row['week']
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item

        yield self.request_next(fps, ips)
