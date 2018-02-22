# -*- coding: utf-8 -*-
from datetime import datetime

from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class JiShengInvestSpider(GGFundNavSpider):
    name = 'FundNav_JiShengInvest'
    sitename = '季胜投资'
    channel = '投顾净值'
    allowed_domains = ['www.jishengtouzi.com']
    start_urls = ['http://www.jishengtouzi.com/index.aspx']

    def __init__(self, *args, **kwargs):
        super(JiShengInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        ips = [
            {
                'url': 'http://www.jishengtouzi.com/jsdata.aspx',
                'ref': None
            }
        ]

        yield self.request_next([], ips)

    def parse_item(self, response):
        data_all = response.text.split(';')
        for data in data_all:
            fund_name = None
            if str(data).startswith('var jz_date'):
                fund_name = '平安信托金蕴55期季胜投资基金'
            if str(data).startswith('var fq_date'):
                fund_name = '中欧盛世季胜1号投资基金'
            if fund_name is not None:
                list_all = data[23:-3].split('],[Date.UTC(')
                for i in list_all:
                    statistic_date = i.split('),')[0]
                    statistic_date = datetime.strptime(statistic_date, '%Y,%m,%d')
                    nav = i.split('),')[1]

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = statistic_date
                    item['nav'] = float(nav)
                    yield item
