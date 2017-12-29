# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SmileStoneSpider(GGFundNavSpider):
    name = 'FundNav_SmileStone'
    sitename = '理成资产'
    channel = '投资顾问'
    allowed_domains = ['www.smilestone.com.cn']
    start_urls = ['http://www.smilestone.com.cn/member']

    def __init__(self, limit=None, *args, **kwargs):
        super(SmileStoneSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.smilestone.com.cn/Router.php?action=MemberController/searchHotProduct/tableQuery',
                'form': {'hot_type': '1', 'pageNum': '1', 'rowCount': '100'},
                'ref': 'http://www.smilestone.com.cn/member',
                'cookies': 'PHPSESSID=fvalg5f50pagd1c6aoafp0p824; lczc_cpbg_new=0; lczc_wdtw_new=0; td_cookie=11049181'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = json.loads(response.text)['data']
        for fund in funds:
            ips.append({
                'url': 'http://www.smilestone.com.cn/Router.php?action=MemberController/searchNetvalue',
                'form': {'pcode': fund['pcode']},
                'ref': response.request.headers['Referer']
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = json.loads(response.text)['data']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = row['pname']

            statistic_date = row['valuetime']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = row['value']
            item['added_nav'] = row['totalvalue']
            yield item

        yield self.request_next(fps, ips)
