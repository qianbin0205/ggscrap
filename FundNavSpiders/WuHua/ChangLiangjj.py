import json
# from datetime import datetime
import time
import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
from scrapy import Request


class ChangLiangjjSpider(GGFundNavSpider):
    name = 'FundNav_ChangLiangjj'
    sitename = '长量基金'
    channel = '投资顾问'
    allowed_domains = ['www.erichfund.com']

    def __init__(self, limit=None, *args, **kwargs):
        super(ChangLiangjjSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.erichfund.com/pubweb/websiteII/LoadPrivateFund',
                'ref': 'http://www.erichfund.com/pubweb/websiteII/PrivateFund',
                'headers': {
                    'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Content-Type':'application/json; charset=UTF-8',
                    'X-Requested-With':'XMLHttpRequest'
                },
                'body': '{"privateType":"","start":1,"limit":100}'
            }
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fundList = json.loads(response.text)["list"]
        ips = []
        for fund in fundList:
            fundid = fund["fundid"]
            fundname = fund["fundnm"]
            ips.append(
                    {
                        'url': 'http://www.erichfund.com/pubweb/websiteII/LoadPrivateFundNetValue',
                        'ref': 'Referer:http://www.erichfund.com/pubweb/websiteII/PrivateDetail/'+fundid,
                        'headers': {
                            'Accept':'application/json, text/javascript, */*; q=0.01',
                            'Content-Type':'application/json; charset=UTF-8',
                            'X-Requested-With':'XMLHttpRequest'
                        },
                        'body': '{"fundId":"'+fundid+'","start":1,"limit":100}',
                        'ext': {'fund_name': fundname}
                    }
            )

        yield self.request_next([], ips)

    def parse_item(self, response):
        ext = response.meta['ext']
        nvList = json.loads(response.text)["list"]
        # ltime=time.localtime(1395025933)
        # timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        # print(timeStr)
        # print(nvList)
        for nv in nvList:
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = ext['fund_name']
            init_date = nv['navdate']
            # print(init_date)
            ldate = time.localtime(init_date/1000)
            dateStr=time.strftime("%Y-%m-%d %H:%M:%S", ldate)
            # print(dateStr)
            item['statistic_date'] = datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
            nav = nv['nav']
            item['nav'] = float(nav) if nav is not None else None
            added_nav = nv['sumofnav']
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item
        yield self.request_next()
