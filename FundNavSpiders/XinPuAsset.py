# -*- coding: utf-8 -*-

import json
from urllib.parse import quote
from datetime import datetime
from scrapy import Request
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class XinPuAssetSpider(GGFundNavSpider):
    name = 'FundNav_XinPuAsset'
    sitename = '信普资产'
    channel = '投顾净值'
    allowed_domains = ['www.xinpibao.com']
    start_urls = ['http://www.xinpibao.com/company/M11451.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(XinPuAssetSpider, self).__init__(limit, *args, **kwargs)

    # def parse_pre_login(self, response):
    #     yield Request(url='http://www.xinpibao.com/sso/api/users/login',
    #                   method='POST',
    #                   headers={'Content-Type': 'application/x-www-form-urlencoded',
    #                            'Referer': 'http://www.xinpibao.com/sso/'},
    #                   body=b'{"mobile":"13916427906","password":"ZYYXSM123"}',
    #                   callback=self.parse_login)
    #
    # def parse_login(self, response):
    #     pass

    def start_requests(self):
        # yield Request(url='http://www.xinpibao.com/sso/api/users/random', callback=self.parse_pre_login)

        cookies = self.parse_cookies('td_cookie=11049239; JSESSIONID=83E585FFB36F48C49A2227DC43333A81; Hm_lvt_bd5f74e276d37b338277623405760296=1514455130,1516003028,1516003103; xpbtoken=128068db2nlq4fmuhg88rthg9eeoc; Hm_lpvt_bd5f74e276d37b338277623405760296=1516014521')
        yield Request(url='http://www.xinpibao.com/web/api/idmapping/?id=M11451', cookies=cookies,
                      callback=self.parse_map)

    def parse_map(self, response):
        flt = '{"managerCompanyId":"' + eval(response.text)['data'] + '"}'
        flt = quote(flt)

        fps = [
            {
                'url': 'http://www.xinpibao.com/web/api/funds/computeInfos/?filter=' + flt + '&from=0',
                'ref': 'http://www.xinpibao.com/company/M11451.html',
                # 'cookies': 'td_cookie=11049239; JSESSIONID=83E585FFB36F48C49A2227DC43333A81; Hm_lvt_bd5f74e276d37b338277623405760296=1514455130,1516003028,1516003103; xpbtoken=128068db2nlq4fmuhg88rthg9eeoc; Hm_lpvt_bd5f74e276d37b338277623405760296=1516014521'
                # 'headers': {'Accept': 'application/json, text/javascript, */*; q=0.01',
                #             'Accept-Encoding': 'gzip, deflate',
                #             'Accept-Language': 'zh-CN,zh;q=0.9',
                #             'X-Requested-With': 'XMLHttpRequest'}
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
                'url': lambda pg: 'http://xinpibao.com/web/api/funds/' + str(pg['fund_id']) + '/netValues?from=' + str(
                    6 * pg['page']),
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
        if 6 * pg['page'] < total:
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
