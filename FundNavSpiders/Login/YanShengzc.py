import json
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy import FormRequest


class YanShengzcSpider(GGFundNavSpider):
    name = 'FundNav_YanShengzc'
    sitename = '衍盛资产'
    channel = '投资顾问'
    allowed_domains = ['derivatives-china.invest.ldtamp.com']

    username = '13916427906'
    password = 'ZYYXSM123'

    start_urls = []
    fps = [
        {
            'url': 'http://derivatives-china.invest.ldtamp.com/pfL.1.201.json',
            'ref': None,
            'form': {'risk_accept': '4', 'invester_class': '1', 'row_count': '-1'}
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(YanShengzcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://derivatives-china.invest.ldtamp.com/customerPassWordLogin.do',
                          formdata={'cust_loginname': '18603799126', 'cust_passwd': '33a60087e96a3c62cdc306a2ba2f1653',
                                    'row_count': '-1'},
                          headers={'Accept': 'application/json, text/javascript, */*; q=0.01'},
                          callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        funds = json.loads(response.text)['result']
        date = datetime.strftime(datetime.now(), '%Y%m%d')
        ips = []
        for fund in funds:
            ips.append({
                'url': 'http://derivatives-china.invest.ldtamp.com/pfL.1.203.json',
                'ref': None,
                'form': {'qry_begin_date': '0', 'qry_end_date': date, 'pd_no': str(fund["pd_no"]),
                         'official_art_type': '2', 'row_count': '-1'}
            })

            yield self.request_next([], ips)

    def parse_item(self, response):
        nvList = json.loads(response.text)['result']
        for eachNv in nvList:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = eachNv['pd_name']
            init_date = eachNv['init_date']
            statistic_date = str(init_date)[:4] + '-' + str(init_date)[4:6] + '-' + str(init_date)[6:8]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = eachNv['share_net']
            item['nav'] = float(nav) if nav is not None else None
            added_nav = eachNv['share_net_total']
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item
