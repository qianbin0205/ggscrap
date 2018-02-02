import json
from datetime import datetime
from scrapy import Request
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class JuShanzcSpider(GGFundNavSpider):
    name = 'FundNav_JuShanzc'
    sitename = '巨杉资产'
    channel = '投资顾问'
    allowed_domains = ['www.grasset.com.cn']

    fps = [
        {
            'url': 'http://www.grasset.com.cn/api/product/queryNetValueList',
            'headers': {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8'
            },
            'body': '{"auditStatus":3,"productType":"","productName":""}',
            'ref': 'http://www.grasset.com.cn/productNetValueList'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(JuShanzcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.grasset.com.cn/api/login/login',
                      method='post',
                      headers={'Content-Type': 'application/json',
                               'Referer': 'http://www.grasset.com.cn/auth'
                               },
                      body=b'{"loginName":"13916427906","password":"123456"}',
                      callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        data = json.loads(response.text)['data']

        for record in data['records']:
            fund_id = record['productId']
            fund_name = record['productName']
            self.ips.append({
                'pg': {'page': 1, 'fund_id': fund_id},
                'url': 'http://www.grasset.com.cn/api/product/netValue/query',
                'headers': {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json;charset=UTF-8'
                },
                'body': lambda pg: '{"pageSize":500,"pageNumber":' + str(pg['page']) + ',"productId":"' + pg['fund_id'] + '"}',
                'ref': 'http://www.grasset.com.cn/productNetValueDetail/' + fund_id,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next()

    def parse_item(self, response):
        data = json.loads(response.text)['data']
        ext = response.meta['ext']

        fund_name = ext['fund_name']
        for record in data['records']:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = record['netDate'][0:10]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = record['netValue']
            item['added_nav'] = record['netValueAccu']
            yield item

        pg = response.meta['pg']
        if pg['page'] * 500 < int(data['totalRecordCount']):
            pg['page'] = pg['page'] + 1
            self.ips.append({
                'pg': pg,
                'url': response.url,
                'headers': response.meta['headers'],
                'body': response.meta['body'],
                'ref': response.meta['ref'],
                'ext': response.meta['ext']
            })

        yield self.request_next()
