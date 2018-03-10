# -*- coding: utf-8 -*-
from datetime import datetime
import time
import json
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShiTianFengInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShiTianFengInvest'
    sitename = '北京时田丰投资'
    channel = '投顾净值'
    allowed_domains = ['www.shitianfeng.com']

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = '__AntiXsrfToken=cc64828bc5c144d192f9f4672f38fe9b; ValidateCode=T7XTQ; .AspNet.ApplicationCookie=BMNuRP132bYZoa7dfFCch20RaVGX4OR362IA6gGRhx-_zu6w39RIrQv4-4IevoYf3hN4FlgqGk6CPOl4EH5M7gO5ZuzDDH9tB4-Mne_C5pFK2Sj-Xyw8wPmxP7Cn96PeRGrES-I6Mgk2WIKvvERjto0dw-neSlhS0BMc1TNmcLPhNx_-6UQhymvMWGvOK4CGN-gbIkOI3PbmO6hBOzMKr9CL5jAmdmDSQnspFUAa7XqkKcJdNxm0NU7NSjfRIdu7zvEkjC3lQ8LD56H2BHXQ9AwgxOu4sQmrnAiRYHVp6WEVsmpuFiscWeWHmuhhHmIrF5FdWg4fK7Q_ZKbT56IXgAKGET8Ens92VKdQCYjDdrpf7V3Iv4ggGoPP-qJleqoagRfAL96zMwgmrRL1vfTeiMfmvmAbD7O33mpe8anGO7U7UN2j-UhOAe8fdk-RrOosm9L5hLjJkDVCbloXxYKbtj2Zmg10snIahHi2krZKDzSIsHSUTYc4yOB9_86BPmRhp1PUBwO36gG82E5c9akM5Q'
    fps = [{
        'url': 'http://www.shitianfeng.com/Products/ProductList',
        'ref': 'http://www.shitianfeng.com/Default'
    }]

    def __init__(self, *args, **kwargs):
        super(ShiTianFengInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        href_list = response.css('table div.grvrow1 a::attr(href)').extract()
        name_list = response.css('table div.grvrow1 a::text').extract()

        for fund_name, href in zip(name_list, href_list):
            pid = href.split('?')[-1]
            nav_url = 'http://www.shitianfeng.com/Products/getproductvalue.ashx?' + pid
            self.ips.append({
                'url': nav_url,
                'ref': response.url,
                'ext': {
                    'fund_name': fund_name
                }
            })

        yield self.request_next()

    def parse_item(self, response):
        rows = json.loads(response.text)
        fund_name = response.meta['ext']['fund_name']

        for row in rows:
            stamp = row[0]
            nav = row[1]
            date = time.strftime("%Y-%m-%d", time.localtime(int(stamp)/1000))

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)/100
            item['added_nav'] = None
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
            yield item

        yield self.request_next()
