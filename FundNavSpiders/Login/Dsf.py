# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class DsfSpider(GGFundNavSpider):
    name = 'FundNav_Dsf'
    sitename = '德盛期货'
    channel = '发行机构'
    allowed_domains = ['www.dsf.cn']
    start_urls = ['http://www.dsf.cn/dsqh/zcgl/zgcp/index.shtml']

    def __init__(self, limit=None, *args, **kwargs):
        super(DsfSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.dsf.cn/dsqh/jsp/appoint/passport.jsp',
                          formdata={'contact': '17839170174',
                                    'password': '123456'},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.dsf.cn/dsqh/zcgl/zgcp/index.shtml',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('script').re(r'json\[\d+?\]\s*=\s*([^;]+)\s*;')

        for fund in funds:
            fund = eval(fund)
            url = re.sub(r'<a\s+?href="([^<>"]+/)cpjs(/[^<>"]+)">[^<>]+?</a>', r'\1cpjz\2', fund['title'])
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = response.css('script').re(r'json\[\d+?\]\s*=\s*([^;]+)\s*;')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            row = eval(row)
            item['fund_name'] = row['title']

            statistic_date = row['addtime']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row['dc1'])
            item['added_nav'] = float(row['dc2'])

            yield item

        yield self.request_next(fps, ips)
