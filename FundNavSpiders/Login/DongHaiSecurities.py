# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class DongHaiSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_DongHaiSecurities'
    sitename = '东海证券'
    channel = '券商资管净值'
    allowed_domains = ['www.longone.com.cn']

    username = '13916427906'
    password = 'ZYYXSM123'
    start_urls = ['http://www.longone.com.cn/']

    def __init__(self, *args, **kwargs):
        super(DongHaiSecuritiesSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.longone.com.cn/servlet/user/Login?function=AjaxLogin',
                          headers={'Referer': 'http://www.longone.com.cn/main/index.html'},
                          formdata={
                              'uname': '13916427906',
                              'upwd': '2541249b0016101d94c93e98914728a3972977091fa211ea55d1ecc8fc160d5b439694a0b0516894e44481e278f73d1efb8a894f3252607e707172a263bd2e7edfd2935617904fa63bdc5c5030cab4e8e85001c0141eb08667f15e05941c57e087b1abc5c61765cd9f01b875fbcd6171cfe05ec1a62383e565bd86c7cf087f28',
                              'inpjs': 'jsfsa'
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps.append({
            'url': 'http://www.longone.com.cn/main/assetmanage/product/index.html',
            'ref': 'http://www.longone.com.cn/main/assetmanage/index.html'
        })
        yield self.request_next()

    def parse_fund(self, response):
        funds = response.xpath('//ul[@id="child_3187"]/li/a')
        for fund in funds:
            fund_code = fund.css('::attr(name)').re_first(r'/main/assetmanage/subproduct/([^/]+)/index.html')
            fund_name = fund.css('span').re_first(r'>\s*([^<>\s]+)\s*<')
            self.ips.append({
                'url': 'http://www.longone.com.cn/cgi-bin/asset/AssetManage?function=AjaxUnit&i_fund_code={0}&i_start_date=2000-01-01&i_end_date=&fundcode_nochang={0}'.format(
                    fund_code),
                'ref': 'http://www.longone.com.cn/main/assetmanage/subproduct/{}/index.html'.format(fund_code),
                'ext': {'fund_name': fund_name}
            })

            self.ips.append({
                'url': 'http://www.longone.com.cn/cgi-bin/asset/AssetManage?function=GetProductType&fundCode={0}'.format(
                    fund_code),
                'ref': 'http://www.longone.com.cn/main/assetmanage/subproduct/{0}/index.html'.format(fund_code),
                'ext': {'fund_code': fund_code}
            })

        yield self.request_next()

    def parse_item(self, response):
        ext = response.meta['ext']
        resp = json.loads(response.text)
        if 'fund_name' in ext:
            if 'data' in resp:
                rows = resp['data']['list']
                for row in rows:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = ext['fund_name']
                    item['nav'] = float(row['nav'])
                    item['added_nav'] = float(row['totalnav'])
                    statistic_date = row['settledate']
                    statistic_date = datetime.strptime(statistic_date, '%Y%m%d')
                    item['statistic_date'] = statistic_date
                    yield item
        else:
            if 'fundData' in resp['data']:
                sub = resp['data']['fundData']['sub_content']
                if sub:
                    funds = re.findall(r'([^:#\s]+:[^:#\s]+#\d+-\d+)\s*(?:,|$)', sub)
                    for fund in funds:
                        m = re.search(r'([^:#\s]+):([^:#\s]+)#\d+-\d+\s*(?:,|$)', fund)
                        fund_name = m.group(1)
                        fund_code = m.group(2)
                        self.ips.append({
                            'url': 'http://www.longone.com.cn/cgi-bin/asset/AssetManage?function=AjaxUnit&i_fund_code={0}&i_start_date=2000-01-01&i_end_date=&fundcode_nochang={1}'.format(
                                fund_code, ext['fund_code']),
                            'ref': 'http://www.longone.com.cn/main/assetmanage/subproduct/{}/index.html'.format(
                                ext['fund_code']),
                            'ext': {'fund_name': fund_name}
                        })

        yield self.request_next()
