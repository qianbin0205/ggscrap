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
    cookies = 'JSESSIONID=C6A4A487A8EB7D728B47E0C5EC080915; Hm_lvt_099ede35125085b13b2ce845fff55d0a=1517289571; Hm_lpvt_099ede35125085b13b2ce845fff55d0a=1517289584; Hm_lvt_e75c81301e11720191cdfb53e718f25b=1517289571; Hm_lpvt_e75c81301e11720191cdfb53e718f25b=1517289584'

    def __init__(self, limit=None, *args, **kwargs):
        super(HuaAnzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://pb.hazq.com:6384/quick4j/rest/user/data/prod',
                'ref': None
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        # print(response.text)
        fundList = json.loads(response.text)
        for fund in fundList:
            print(fund["prodName"])
