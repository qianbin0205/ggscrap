import json
from scrapy import FormRequest, Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class FreedChinaSpider(GGFundNavSpider):
    name = 'FundNav_FreedChina'
    sitename = '北京福睿德投资'
    channel = '投顾净值'
    allowed_domains = ['www.freedchina.com']
    start_urls = ['http://www.freedchina.com/Products/index']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.freedchina.com/Products/index',
        'Ref': 'http://www.freedchina.com/Home/Index/index'
    }]

    def __init__(self, *args, **kwargs):
        super(FreedChinaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.freedchina.com/Login/login',
                          headers={'Referer': 'http://www.freedchina.com/join/index'},
                          formdata={
                              'username': '13916427906',
                              'password': 'ZYYXSM123'
                          },
                          meta={
                              'handle_httpstatus_list': [302]
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield Request(url='http://www.freedchina.com/ti/agree/status/agree',
                      callback=self.prase_pro_login)

    def prase_pro_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fund_list = response.xpath('//div[@class="fl w260"]//li//a/text()').extract()
        link_list = response.xpath('//div[@class="fl w260"]//ul//li/a/@href').extract()

        for name, link_key in zip(fund_list, link_list):
            if '千石资本-海通MOM私募精选之福睿...' in name:
                fund_name = '千石资本-海通MOM私募精选之福睿德3号'
            else:
                fund_name = name

            fund_code = link_key.split('/')[-1]
            self.ips.append({
                'url': 'http://www.freedchina.com/Home/Products/getNet?page=' + '0' + '&pid=' + fund_code,
                'ref': response.url,
                'ext': {'fund_name': fund_name},
                'pg': 0
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        nav_json = json.loads(response.text)
        nav_list = nav_json['list']

        if nav_list:
            for n in nav_list:
                statistic_date = n['time']
                nav = n['net']
                added_nav = n['total']

                if statistic_date:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                    item['nav'] = float(nav) if nav is not None else None
                    item['added_nav'] = float(added_nav) if added_nav is not None else None

                    yield item

            page = response.meta['pg']
            next_pg = page + 1
            url = response.url.replace('?page=' + str(page), '?page=' + str(next_pg))
            self.ips.append({
                'url': url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name},
            })

        yield self.request_next()
