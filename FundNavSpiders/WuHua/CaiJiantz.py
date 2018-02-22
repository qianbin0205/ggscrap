import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
from scrapy import Request


class CaiJiantzSpider(GGFundNavSpider):
    name = 'FundNav_CaiJiantz'
    sitename = '上海财健投资'
    channel = '投资顾问'
    allowed_domains = ['www.caijianfund.com']
    cookies = 'PHPSESSID=q53p0odq6ng1ebrjl2emd84er5'

    def __init__(self, limit=None, *args, **kwargs):
        super(CaiJiantzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.caijianfund.com/Fund_getHistory.html?p=1&fund_id=1&start_date=&end_date=',
                'ref': None
            }
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fundList = json.loads(response.text)["content"]
        for fund in fundList:
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = '财健双赢1期私募投资基金'
            init_date = fund['jzrq']
            item['statistic_date'] = datetime.strptime(init_date, '%Y-%m-%d')
            nav = fund['dwjz']
            item['nav'] = float(nav) if nav is not None else None
            added_nav = fund['ljjz']
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item

