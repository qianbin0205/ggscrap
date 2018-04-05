# -*- coding: utf-8 -*-
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class DeBangZhengQuanSpider(GGFundNavSpider):
    name = 'FundNav_DeBangZhengQuan'
    sitename = '德邦证券'
    channel = '券商资管净值'
    allowed_domains = ['www.tebon.com.cn']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.tebon.com.cn/dbzq/zcgl/cpjz.jsp?classid=00010001000600040001',
            'Referer': 'http://www.tebon.com.cn/dbzq/zcgl/JSONInfo.jsp?classid=000100010006000400020005'}]

    def __init__(self, *args, **kwargs):
        super(DeBangZhengQuanSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        fund_code = response.css('select.select120 option::attr(value)').extract()
        fund_name = response.css('select.select120 option::text').re('-+\s+(.*?)\s+-+')
        for c, n in zip(fund_code, fund_name):
            self.ips.append({
                'url': 'http://www.tebon.com.cn/dbzq/zcgl/data/jhjzData.jsp?code={}'.format(c),
                'ref': response.url,
                'ext': {'fund_name': n}
            })
        yield self.request_next()

    def parse_item(self, response):
        js_data = json.loads(''.join(response.text.split()))
        fund_name = response.meta['ext']['fund_name']
        rows = js_data['elements'][0]['values']

        for row in rows:
            r = row['tip'].split('<br>')
            nav = row['value']
            added_nav = r[0]
            statistic_date = r[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        yield self.request_next()
