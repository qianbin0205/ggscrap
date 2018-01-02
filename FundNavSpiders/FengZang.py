# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class FengZangSpider(GGFundNavSpider):
    name = 'FundNav_FengZang'
    sitename = '丰奘投资'
    channel = '投资顾问'
    allowed_domains = ['www.fengzang.com.cn']
    start_urls = ['http://www.fengzang.com.cn/HBBKTZ/qian/center.jsp']

    def __init__(self, limit=None, *args, **kwargs):
        super(FengZangSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(
            url='http://www.fengzang.com.cn/HBBKTZ/dt/jsonHbbkDtMainJsonAction_qloginOneHbbkDtMain.action',
            formdata={'maintitle': '123456',
                      'mainjian': '123456'},
            callback=self.parse_login)

    def parse_login(self, response):
        ips = [
            {
                'url': 'http://www.fengzang.com.cn/HBBKTZ/dt/jsonHbbkDtMainJsonAction_qgetpmHbbkDtMain.action',
                'form': {'page': '1', 'limit': '160', 'maintitle': '', 'maintype': '10'},
                'ref': 'http://www.dctstz.com/',
                'ext': {'fund_name': '丰奘1号'}
            },
            {
                'url': 'http://www.fengzang.com.cn/HBBKTZ/dt/jsonHbbkDtMainJsonAction_qgetpmHbbkDtMain.action',
                'form': {'page': '1', 'limit': '160', 'maintitle': '', 'maintype': '11'},
                'ref': 'http://www.dctstz.com/',
                'ext': {'fund_name': '丰奘2号'}
            },
            {
                'url': 'http://www.fengzang.com.cn/HBBKTZ/dt/jsonHbbkDtMainJsonAction_qgetpmHbbkDtMain.action',
                'form': {'page': '1', 'limit': '160', 'maintitle': '', 'maintype': '12'},
                'ref': 'http://www.dctstz.com/',
                'ext': {'fund_name': '丰奘3号'}
            }
        ]

        yield self.request_next([], ips)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css(r'.list_product_box>ul>li>a::attr(href)').extract()
        for fund in funds:
            url = urljoin(get_base_url(response), fund)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        ext = response.meta['ext']

        fund_name = ext['fund_name']
        rows = json.loads(response.text)['rows']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row['mainelse2']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['added_nav'] = float(row['mainelse3'])

            yield item

        yield self.request_next(fps, ips)
