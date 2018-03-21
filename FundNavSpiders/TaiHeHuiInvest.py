# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class TaiHeHuiInvestSpider(GGFundNavSpider):
    name = 'FundNav_TaiHeHuiInvest'
    sitename = '北京泰和汇投资'
    channel = '投资顾问'
    allowed_domains = ['www.thhfunds.com']

    fps = [{
        'url': 'http://www.thhfunds.com/?product_category=cpjz',
        'ref': 'https://www.thudamc.com'
    }]

    def __init__(self, *args, **kwargs):
        super(TaiHeHuiInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        nav_url_list = response.css('div.ti.fl a::attr(href)').extract()
        for nav_url in nav_url_list:
            self.ips.append({
                'url': nav_url,
                'ref': response.url
            })
        yield self.request_next()

    def parse_item(self, response):
        name_match = {
            'S81154': '泰和汇1期择时策略混合基金',
            'SN5055': '泰和汇2期主题精选私募投资基金'
        }

        rows = response.css('table tr')
        for row in rows[1:]:
            info = row.css('th ::text').re('\S+')
            if info:
                fund_name = name_match[info[0]]
                statistic_date = info[1]
                nav = info[2]
                added_nav = info[3]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['statistic_date'] = statistic_date
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item

        yield self.request_next()
