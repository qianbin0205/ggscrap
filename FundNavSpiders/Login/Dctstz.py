# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class DctstzSpider(GGFundNavSpider):
    name = 'FundNav_Dctstz'
    sitename = '北京鼎诚同盛投资'
    channel = '投资顾问'
    allowed_domains = ['www.dctstz.com']
    start_urls = ['http://www.dctstz.com/index.php?m=content&c=index&a=lists&catid=8']

    def __init__(self, limit=None, *args, **kwargs):
        super(DctstzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.dctstz.com/index.php?m=users&c=index&a=login',
                          formdata={'login_u_mobile': '13916427906',
                                    'login_u_password': 'ZYYXSM123'},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.dctstz.com/index.php?m=content&c=index&a=lists&catid=8',
                'ref': 'http://www.dctstz.com/',
            }
        ]

        yield self.request_next(fps, [])

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

        if re.search(r'&year=\d+', response.url) is None:
            years = response.css('#year>option:not([selected="selected"])::attr(value)').extract()
            for year in years:
                ips.append({
                    'url': response.url + '&year=' + year,
                    'ref': response.url
                })

        fund_name = response.css('.show_product h3::text').extract_first()
        data = response.css('script').re_first(r'var\s*?json_charts\s*?=\s*?([^;]+)[\s;]*?var\s*?years\s*?=')
        rows = json.loads(data)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row['c_date']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row['c_large'])
            item['added_nav'] = float(row['c_accnav'])

            yield item

        yield self.request_next(fps, ips)
