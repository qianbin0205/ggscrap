import json
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
import re


class DingXinHuiJinSpider(GGFundNavSpider):
    name = 'FundNav_DingXinHuiJin'
    sitename = '北京鼎信汇金投资'
    channel = '投顾净值'
    allowed_domains = ['www.9ifund.com']
    start_urls = ['https://www.9ifund.com/sm/one.html']

    account = '15838867575'
    password = '123456'

    def __init__(self, *args, **kwargs):
        super(DingXinHuiJinSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.fps = [
            {'url': 'https://www.9ifund.com/sm/one.html'}
        ]
        yield self.request_next()

    def parse_fund(self, response):
        link_key = response.xpath('//div[@class = "mainw"]//ul//li//a/@id').extract()
        for key in link_key:
            link = 'https://oa.tl50.com/api/api.fund.sms/fund_net_q?fund_code=' + key + '&limit=200&page=1'
            self.ips.append({
                'url': link,
                'ref': response.url,
                'pg': 1
            })
        yield self.request_next()

    def parse_item(self, response):
        info_json = json.loads(response.text)
        fund_nets = info_json['data']['fund_nets']
        if 'page=1' in response.url:
            fund_name = info_json['data']['fund_info']['fund_name']
        else:
            fund_name = response.meta['ext']['fund_name']
        if fund_nets:
            for nets in fund_nets:
                statistic_date = nets['net_date']
                nav = nets['pemet_value']
                added_nav = nets['total_net']

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item
            next_pg = response.meta['pg'] + 1
            next_link = re.sub('\d+$', str(next_pg), response.url)
            self.ips.append({
                'url': next_link,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next()
