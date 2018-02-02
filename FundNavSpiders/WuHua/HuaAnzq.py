import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy import FormRequest


class HuaAnzqSpider(GGFundNavSpider):
    name = 'FundNav_HuaAnzq'
    sitename = '华安证券（总）'
    channel = '券商PB净值列表'
    allowed_domains = ['pb.hazq.com:6384']
    # start_urls = ['http://derivatives-china.invest.ldtamp.com/pfL.1.201.json']
    cookies = 'JSESSIONID=37D924810E2CE39CB17DFD7333AC81B6; Hm_lvt_099ede35125085b13b2ce845fff55d0a=1517289571; Hm_lvt_e75c81301e11720191cdfb53e718f25b=1517289571'

    def __init__(self, limit=None, *args, **kwargs):
        super(HuaAnzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://pb.hazq.com:6384/quick4j/rest/user/data/prod',
                'ref': None
            }
        ]

        yield self.request_next(fps)

    def parse_fund(self, response):
        fundList = json.loads(response.text)
        for fund in fundList:
            nvList = fund['netValue'].split('<br/>')
            if len(nvList) == 1:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund['prodName']
                init_date = fund['netDate']
                statistic_date = str(init_date)[:4]+'-'+str(init_date)[4:6]+'-'+str(init_date)[6:8]
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                nav = fund['netValue']

                item['nav'] = float(nav) if nav is not None else None
                added_nav = fund['cumulativeNetValue']
                item['added_nav'] = float(added_nav)if added_nav is not None else None
                yield item
            else:
                for eachNv in nvList:
                    eachNvInfo = eachNv.split(':')
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund['prodName']+"--"+eachNvInfo[0]
                    init_date = fund['netDate']
                    statistic_date = str(init_date)[:4]+'-'+str(init_date)[4:6]+'-'+str(init_date)[6:8]
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                    # nav = fund['netValue']
                    item['nav'] = float(eachNvInfo[1]) if nav is not None else None
                    added_nav = fund['cumulativeNetValue']
                    item['added_nav'] = float(added_nav)if added_nav is not None else None
                    yield item
