import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class WanJizcSpider(GGFundNavSpider):
    name = 'FundNav_WanJizc'
    sitename = '万霁资产'
    channel = '产品净值'
    allowed_domains = ['www.wanjizichan.com']
    start_urls = ['http://www.wanjizichan.com/products']
    # url = 'http://www.wanjizichan.com'

    def __init__(self, limit=None, *args, **kwargs):
        super(WanJizcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.wanjizichan.com/1.0/products',
                'ref': None,
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        # print(response.text)
        funds = json.loads(response.text)
        item = GGFundNavItem()

        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url

        for fund in funds:
            # print(data)
            item['fund_name'] = fund['name']
            # print(fund['jzDataInfo'])
            nvDatas = fund['jzDataInfo']
            for nvData in nvDatas:
                print(nvData['date'])
                statistic_date = nvData['date']
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

                nav = nvData['dwValue']
                item['nav'] = float(nav) if nav is not None else None

                added_nav = nvData['value']
                item['added_nav'] = float(added_nav)if added_nav is not None else None
                yield item
