import re
import json
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from datetime import datetime


class ShengangSecuritiesAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShengangSecuritiesAsset'
    sitename = '申港证券资产管理部'
    channel = '发行机构'
    allowed_domains = ['zcgl.shgsec.com']

    start_urls = []
    fps = [
        {
            'url': 'http://zcgl.shgsec.com/front/apiv1/asset/asset.jsp?cmd=listProduct&status=2&font=1',
            'ref': 'http://zcgl.shgsec.com/sgzq-new/sgzq_zcgl/index.html'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(ShengangSecuritiesAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://zcgl.shgsec.com/sgzq-new/sgzq_zcgl/index.html', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://zcgl.shgsec.com/front/apiv1/user/login2.jsp',
                          formdata={'username': '13916427906',
                                    'password': 'ZYYXSM123',
                                    'cmd': 'LoginForQT',
                                    'check': 'false'
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = json.loads(response.text)
        for fund in funds[1:]:
            pid = fund['_id']
            fundInfoUrl = 'http://zcgl.shgsec.com/front/apiv1/asset/asset.jsp?cmd=listNetWorth&count=99999&from=1&dir=-1&PID=' + pid
            ips.append({
                'url': fundInfoUrl,
                'ref': response.url,
            })

        yield self.request_next([], ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']

            datas = json.loads(response.text)
            for data in datas[1:]:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url

                item['fund_name'] = data['Name']

                statistic_date = data['ValueDate']
                statistic_date = '20'+ str(statistic_date) if statistic_date is not None else None
                statistic_date = datetime.strptime(statistic_date, '%Y%m%d')
                item['statistic_date'] = statistic_date

                nav = data['NetValue']
                nav = re.search(r'([0-9.]+)', str(nav))
                nav = nav.group(0) if nav is not None else None
                item['nav'] = float(nav) if nav is not None else None

                added_nav = data['TotalValue']
                added_nav = re.search(r'([0-9.]+)', str(added_nav))
                added_nav = added_nav.group(0) if added_nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item

            yield self.request_next(fps, ips)