import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy import FormRequest


class YanShengzcSpider(GGFundNavSpider):
    name = 'FundNav_YanShengzc'
    sitename = '衍盛资产'
    channel = '产品净值'
    allowed_domains = ['derivatives-china.invest.ldtamp.com']
    # start_urls = ['http://derivatives-china.invest.ldtamp.com/pfL.1.201.json']
    cookies = '__guid=185857340.924789394216647200.1516684602690.4316; JSESSIONID=356EEB21CD15626836013B4C3E64E992; SESSION=7e59293b-ba22-4e6a-a1ce-84c1edf7a147; monitor_count=2'

    def __init__(self, limit=None, *args, **kwargs):
        super(YanShengzcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://derivatives-china.invest.ldtamp.com/pfL.1.201.json',
                'ref': None,
                'form': {'risk_accept': '4', 'invester_class': '1', 'row_count': '-1'}
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        # print(response.text)
        funds = json.loads(response.text)['result']
        # print(funds)
        date = datetime.strftime(datetime.now(), '%Y%m%d')
        # print(date)
        ips = []
        for fund in funds:
            # print(fund["pd_no"])
            ips.append({
                'url': 'http://derivatives-china.invest.ldtamp.com/pfL.1.203.json',
                'ref': None,
                'form': {'qry_begin_date': '0', 'qry_end_date': date, 'pd_no': str(fund["pd_no"]), 'official_art_type': '2', 'row_count': '-1'}
            })

            yield self.request_next([], ips)
        # print(ips)

    def parse_item(self, response):
        # print(response.text)
        nvList = json.loads(response.text)['result']
        # print(nvList)
        item = GGFundNavItem()

        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        for eachNv in nvList:
            item['fund_name'] = eachNv['pd_name']
            init_date = eachNv['init_date']
            # print(init_date)
            # print(str(statistic_date)[:4])
            statistic_date = str(init_date)[:4]+'-'+str(init_date)[4:6]+'-'+str(init_date)[6:8]
            # print(statistic_date)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            # print(item['statistic_date'])
            nav = eachNv['share_net']
            item['nav'] = float(nav) if nav is not None else None
            added_nav = eachNv['share_net_total']
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item
