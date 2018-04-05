from scrapy import FormRequest, Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
from urllib import parse
import json


class CeFuturesSpider(GGFundNavSpider):
    name = 'FundNav_CeFutures'
    sitename = '东航期货'
    channel = '期货净值'
    allowed_domains = ['www.cesfutures.com']
    start_urls = ['https://www.cesfutures.com/RESTfull/cfglzx/jj/0/a5d242d2-55ac-45f6-ba25-ac435828e4aa.json']
    username = '13083790899'
    password = '123456!by'

    fps = [{
        'url': 'https://www.cesfutures.com/RESTfull/cfglzx/jj/0/a5d242d2-55ac-45f6-ba25-ac435828e4aa.json',
        'Ref': 'https://www.cesfutures.com/page/cfglzx/'
    }]

    def __init__(self, *args, **kwargs):
        super(CeFuturesSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        payload = {
            "username": "13083790899",
            "password": "37cf15486f6523a08847eed123aad377"
        }
        yield Request(url='https://www.cesfutures.com/RESTfull/user/login.do',
                      headers={
                          'Referer': 'https://www.cesfutures.com/page/cfglzx/',
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.7 Safari/537.36',
                          'Content-Type': 'application/json;charset=UTF-8',
                      },
                      body=json.dumps(payload),
                      method='POST',
                      callback=self.prase_pro_login)

    def prase_pro_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        text = json.loads(response.text)
        for key in text['data']:
            id = key['id']
            fund_link = 'https://www.cesfutures.com/RESTfull/cfglzx/xq/' + id + '.json'
            self.ips.append({
                'url': fund_link,
                'ref': response.url
            })
        yield self.request_next()

    def parse_item(self, response):

        fund_info = json.loads(response.text)

        fund_name = fund_info['data']['xx']['name']

        for data in fund_info['data']['gk']:
            statistic_date = data['time']
            nav = data['dwjz']
            added_nav = data['ljjz']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

        yield self.request_next()
