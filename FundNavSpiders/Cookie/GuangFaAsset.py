from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import json


class GuangFaAssetSpider(GGFundNavSpider):
    name = 'FundNav_GuangFaAsset'
    sitename = '广发证券'
    channel = '券商资管净值'
    allowed_domains = ['www.gfam.com.cn']

    username = '522101197011052410'
    password = 'ZYYXSM123'
    cookies = 'gfportalsid=s%3Acecc6bf0-42fe-11e8-ae99-df901136c8fd_11244_227382_21.L1ksABC0U5uo2XuAhHoPGu1GKEWesHWM3LM2nQ75y9g; GF_STORE_TRACK=5ad7314da41e863f5e010d9a; gfwebsid=eyJ1c2VyIjp7ImN1c3RuYW1lIjoiWllZWFNNIiwiY3VzdG5vIjoiMTM5MTY0Mjc5MDYiLCJjdXN0bm9MaXN0IjpbIjEzOTE2NDI3OTA2Il0sInBob25lIjoiMTM5MTY0Mjc5MDYiLCJiYXVnaHRQcm9kQ29kZUxpc3QiOltdLCJmdW5kQWNjb3MiOltdLCJpZGVudGl0eW5vIjoiNTIyMTAxMTk3MDExMDUyNDEwIiwiaWRlbnRpdHlUeXBlIjoiMSIsInBhc3N3b3JkIjpudWxsLCJnemNvZGUiOm51bGwsImNsaWVudElkIjpudWxsLCJwZXJpb2RUeXBlIjoiNCIsImludmVzdFR5cGUiOiI1Iiwicmlza0xldmVsIjoiNSIsInVzZXJDYXRlZ29yeSI6IjEiLCJ1c2VyVHlwZSI6MSwic2lnbklkIjpudWxsLCJ1c2VyX3R5cGUiOiIxIn19; gfwebsid.sig=Op9-uIc-O5ejIUCKNSKqRU47NzI'

    def __init__(self, limit=None, *args, **kwargs):
        super(GuangFaAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        self.fps = [
            {'url': 'https://www.gfam.com.cn/product/search_index'}
        ]
        yield self.request_next()

    def parse_fund(self, response):
        json_view = json.loads(response.text)
        for i in json_view:
            fund_code = i['product_code']
            product_name = i['product_name']
            self.ips.append({
                'url': 'https://www.gfam.com.cn/product/unitnets?product_code={}&category=cpzx_jhlc_jhjz&page=1&pageSize=200'.format(
                    fund_code),
                'ref': response.url,
                'pg': 1,
                'ext': product_name
            })
        yield self.request_next()

    def parse_item(self, response):
        pg = response.meta['pg']
        fund_name = response.meta['ext']
        rows = response.css('div.inc_div tbody tr')
        if rows:
            tag = response.css('div.inc_div tr th::text').extract()
            if '份额名称' in tag:
                for r in rows:
                    td = r.css('tr ::text').extract()
                    row = [_.strip() for _ in td if _.strip()]
                    date = row[0]
                    nav = row[3]
                    fund_name = row[2]

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                    item['nav'] = float(nav) if nav is not None else None
                    yield item

            else:
                for r in rows:
                    td = r.css('tr ::text').extract()
                    row = [_.strip() for _ in td if _.strip()]
                    date = row[0]
                    nav = row[1]
                    add_nav = row[2]

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                    item['nav'] = float(nav) if nav is not None else None
                    item['added_nav'] = float(add_nav) if add_nav is not None else None
                    yield item

            next_pg = pg + 1
            self.ips.append({
                'url': re.sub('page=\d+', 'page={}'.format(next_pg), response.url),
                'ref': response.url,
                'pg': next_pg,
                'ext': fund_name
            })

        yield self.request_next()
