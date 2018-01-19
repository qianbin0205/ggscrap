# -*- coding: utf-8 -*-

import json
from datetime import datetime, date
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SZXinhenghuiSpider(GGFundNavSpider):
    name = 'FundNav_SZXinhenghui'
    sitename = '深圳信恒慧投资'
    channel = '投资顾问'
    allowed_domains = ['xhh.invest.ldtamp.com']
    start_urls = ['http://xhh.invest.ldtamp.com/#notice.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(SZXinhenghuiSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://xhh.invest.ldtamp.com/customerPassWordLogin.do',
                          formdata={'cust_loginname': '13916427906',
                                    'cust_passwd': '2b908533b6df7069647b6ce18f5f6545',
                                    'row_count': '-1',
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):
        print(response.text)
        fps = [
            {
                'url': 'http://xhh.invest.ldtamp.com/pfL.1.201.json',
                'form': {'risk_accept': '5', 'invester_class': '1', 'row_count': '-1'},
                'ref': 'http://xhh.invest.ldtamp.com/',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = json.loads(response.text)['result']
        for fund in funds:
            pd_no = str(fund['pd_no'])
            fund_name = fund['pd_name']
            qry_end_date = date.isoformat(date.today()).replace('-', '')
            ips.append({
                'url': 'http://xhh.invest.ldtamp.com/pfL.1.203.json',
                'form': {
                    'qry_begin_date': '0',
                    'qry_end_date': qry_end_date,
                    'pd_no': pd_no,
                    'official_art_type': '2',
                    'row_count': '-1',
                },
                'ref': 'http://xhh.invest.ldtamp.com/#product/basicDetail.html',
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = json.loads(response.text)['result']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = row['pd_name']

            statistic_date = str(row['init_date'])
            statistic_date = statistic_date[0:4] + '-' + statistic_date[4:6] + '-' + statistic_date[6:8]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row['share_net'])
            item['added_nav'] = float(row['share_net_total'])
            yield item

        yield self.request_next(fps, ips)
