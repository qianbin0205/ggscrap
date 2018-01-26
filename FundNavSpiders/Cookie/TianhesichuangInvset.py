# -*- coding: utf-8 -*-

import json
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class TianhesichuangInvsetSpider(GGFundNavSpider):
    name = 'FundNav_TianhesichuangInvset'
    sitename = '天和思创投资'
    channel = '投资顾问'
    allowed_domains = ['www.bjthcapital.com', 'www.xinpibao.com']
    start_urls = ['http://www.bjthcapital.com/', 'http://www.xinpibao.com/company/M12043.html']

    username = '18621041957'
    password = '20078991'
    cookies = 'JSESSIONID=302FA311A49AFAE3383A3C94B0DE760A; td_cookie=11049113; Hm_lvt_bd5f74e276d37b338277623405760296=1516936044,1516936325,1516936337; xpbtoken=11m2pj9a13flm8sjvd1ljt1k7u6il; Hm_lpvt_bd5f74e276d37b338277623405760296=1516944238'

    def __init__(self, limit=None, *args, **kwargs):
        super(TianhesichuangInvsetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.xinpibao.com/web/api/funds/computeInfos/?filter=%7B%22managerCompanyId%22%3A%22CP-929387c6-acd6-48f5-b91e-226a7338bbe5%22%7D&from=0',
                'ref': 'http://www.xinpibao.com/company/M12043.html',
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
                'url': 'http://www.xinpibao.com/web/api/funds/' + fund_id + '/values',
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                },
                'ref': 'http://www.xinpibao.com/fund/' + url_id + '.html',
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = json.loads(response.text)['data']['values']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']
            item['fund_name'] = fund_name

            statistic_date = row['evaluateDate'][0:8]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')

            item['nav'] = float(row['shareUnitValue']) if row['shareUnitValue'] is not None else None
            item['added_nav'] = float(row['shareUnitAccumulateValue']) if row['shareUnitAccumulateValue'] is not None else None
            yield item

        yield self.request_next(fps, ips)
