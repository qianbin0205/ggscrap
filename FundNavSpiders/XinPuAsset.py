# -*- coding: utf-8 -*-

import json
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class XinPuAssetSpider(GGFundNavSpider):
    name = 'FundNav_XinPuAsset'
    sitename = '信普资产'
    channel = '投顾净值'
    allowed_domains = ['xinpibao.com']
    start_urls = ['http://xinpibao.com/company/M11451.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(XinPuAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cookies = 'JSESSIONID=8F341B02391F6365A6358DF0D61D093A; Hm_lvt_bd5f74e276d37b338277623405760296=1515745411,1515745617,1515745634,1515977698; td_cookie=11049129; xpbtoken=2pv8hu9n9rmvgg27079h0561telgv; Hm_lpvt_bd5f74e276d37b338277623405760296=1515982751'
        fps = [
            {
                'url': 'http://xinpibao.com/web/api/funds/computeInfos/?filter=%7B%22managerCompanyId%22%3A%22CP-646100ac-9846-4a4f-bb47-f5bc1683f218%22%7D&from=0',
                'ref': 'http://xinpibao.com/company/M11451.html',
                'cookies': cookies
            },
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = json.loads(response.text)['dataList']
        for fund in funds:
            fund_name = fund['fund']['name']
            url_id = fund['fund']['urlId']
            fund_id = fund['id']
            ips.append({
                'pg': {'page': 0, 'fund_id': fund_id},
                'url': lambda pg: 'http://xinpibao.com/web/api/funds/' + str(pg['fund_id']) + '/netValues?from=' + str(6 * pg['page']),
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                },
                'ref': 'http://xinpibao.com/fund/' + url_id + '.html',
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        url = response.meta['url']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = json.loads(response.text)['dataList']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']
            item['fund_name'] = fund_name

            statistic_date = row['evaluateDate'][0:8]
            statistic_date = statistic_date[0:4] + '-' + statistic_date[4:6] + '-' + statistic_date[6:8]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row['shareUnitValue']) if row['shareUnitValue'] is not None else None
            item['added_nav'] = float(row['shareUnitAccumulateValue']) if row['shareUnitAccumulateValue'] is not None else None

            yield item
        total = json.loads(response.text)['total']
        pg = response.meta['pg']
        if 6*pg['page'] < total:
            pg['page'] += 1
            ips.append({
                'pg': pg,
                'url': url,
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Pragma': 'no-cache'
                },
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name},
            })

        yield self.request_next(fps, ips)
