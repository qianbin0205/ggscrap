# -*- coding: utf-8 -*-
from datetime import datetime
import json
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class ShanXiSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_ShanXiSecurities'
    sitename = '山西证券'
    channel = 'PB'  # 需求未写明
    allowed_domains = ['www.i618.com.cn']
    start_urls = ['http://www.i618.com.cn/gsyw/tgyw/xxpl/index/index.shtml']
    cookies = 'score = 98'

    fps = [{
        'url': 'http://www.i618.com.cn/servlet/json',
        'form': {
            'funcNo': '820010',
            'jjdm': '',
            'manage_id': '',
            'curPage': '1',
            'numPerPage': '500'
        },
        'ref': start_urls[0]
    }]

    def __init__(self, *args, **kwargs):
        super(ShanXiSecuritiesSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        products = json.loads(response.text)['results'][0]['data']

        for p in products:
            self.ips.append({
                'url': 'http://www.i618.com.cn/servlet/json',
                'ref': response.url,
                'form': {
                    'funcNo': '820012',
                    'jjdm': p['jjdm'],
                    'curPage': '1',
                    'numPerPage': '500'
                },
                'ext': {
                    'fund_name': p['jjmc']
                }
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = json.loads(response.text)['results'][0]['data']
        if rows:
            for row in rows:
                nav = row['nav']
                add_nav = row['accumulativenav']
                statistic_date = row['tradedate']

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
                item['nav'] = float(nav) if nav else None
                item['added_nav'] = float(add_nav) if add_nav else None
                yield item

            response.meta['form']['curPage'] = str(int(response.meta['form']['curPage']) + 1)
            self.ips.append({
                'url': 'http://www.i618.com.cn/servlet/json',
                'ref': response.url,
                'form': response.meta['form'],
                'ext': {
                    'fund_name': fund_name
                }
            })

            yield self.request_next()
