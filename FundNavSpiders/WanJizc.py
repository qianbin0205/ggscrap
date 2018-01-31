import json
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class WanJizcSpider(GGFundNavSpider):
    name = 'FundNav_WanJizc'
    sitename = '万霁资产'
    channel = '投资顾问'
    allowed_domains = ['www.wanjizichan.com']

    username = 'ZYYXSM'
    password = '13916427906'

    start_urls = ['http://www.wanjizichan.com/products']

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
        funds = json.loads(response.text)
<<<<<<< HEAD:FundNavSpiders/WuHua/WanJizc.py

        for fund in funds:
            # print(data)
            # print(fund['jzDataInfo'])
            nvDatas = fund['jzDataInfo']
            for nvData in nvDatas:
                item = GGFundNavItem()

                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund['name']
                # print(nvData['date'])
=======
        for fund in funds:
            nvDatas = fund['jzDataInfo']
            for nvData in nvDatas:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url

                item['fund_name'] = fund['name']

>>>>>>> 6f2eb72837bea3f296d2b41f62b1a18e99a16244:FundNavSpiders/WanJizc.py
                statistic_date = nvData['date']
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

                nav = nvData['dwValue']
                item['nav'] = float(nav) if nav is not None else None

                added_nav = nvData['value']
                item['added_nav'] = float(added_nav)if added_nav is not None else None
                yield item
