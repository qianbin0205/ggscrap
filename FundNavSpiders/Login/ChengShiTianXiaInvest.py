# -*- coding: utf-8 -*-
from datetime import datetime
import json
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ChengShiTianXiaInvestSpider(GGFundNavSpider):
    name = 'FundNav_ChengShiTianXiaInvest'
    sitename = '北京晟视天下投资'
    channel = '投顾净值'
    allowed_domains = ['www.shengshiview.com']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'https://fund.shengshiview.com/fund/fundController/selectFundInfoList.do',
        'form': {
            'pageNo': '1',
            'pageSize': '300',
            'fundType': '0',
        }
    }]

    def __init__(self, *args, **kwargs):
        super(ChengShiTianXiaInvestSpider, self).__init__(*args, **kwargs)

    def parse_login(self):
        yield FormRequest(url='https://fund.shengshiview.com/login/LoginController/Login.do',
                          formdata={
                              'result': '''15df7c59bf1772c342067d7910b9555e6fc76fb200548ff99
                              0431af99d99bfc94b1f6bb5f2eba288dec48c28a2d0ed5576b86cf1a9576ce
                              fbad698d56850dccfc8ea9ba7e25b3959a6781fc445e39bda005bc7411d8c8
                              70dfb738dea8387016195fb481f7cd372ae782d0df27850d1aa0504ea074c3
                              432a70a336cd1f7005ee9'''
                          },
                          callback=self.start_requests)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        data = json.loads(response.text)
        fund_list = data['cmnFundList']
        if fund_list:
            for f in fund_list:
                fund_name = f['fundName']
                fund_code = f['fundCode']
                end_dt = f['downLoaddate']
                try:
                    start_dt = datetime.strftime(datetime.strptime(f['fundEstablishDate'], '%Y%m%d'), '%Y-%m-%d')
                except KeyError:
                    start_dt = '1990-01-01'

                self.ips.append({
                    'url': 'https://fund.shengshiview.com/fund/FundController/getFundNetValueAccumNet.do',
                    'form': {
                        'fundCode': fund_code,
                        'startDate': start_dt,
                        'endDate': end_dt
                    },
                    'ext': {
                        'fund_name': fund_name
                    }
                })

            new_form = response.meta['form']
            new_form['pageNo'] = str(int(response.meta['form']['pageNo']) + 1)
            self.fps.append({
                'url': 'https://fund.shengshiview.com/fund/fundController/selectFundInfoList.do',
                'form': new_form
            })
        yield self.request_next()

    def parse_item(self, response):
        rows = json.loads(response.text)['data']['rows']
        fund_name = response.meta['ext']['fund_name']

        if rows:
            for row in rows:
                nav = row['UNIT_NET']
                statistic_date = row['DECLAREDATE']
                try:
                    added_nav = row['ACCUM_NET']
                except KeyError:
                    added_nav = None

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav) if added_nav else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

        yield self.request_next()
