import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class NewtfSpider(GGFundNavSpider):
    name = 'FundNav_Newtf'
    sitename = '新同方'
    channel = '投资顾问'
    allowed_domains = ['www.newtf.com']

    username = '13916427906'
    cookies = 'td_cookie=11049132; pgv_pvi=9315215360; pgv_si=s2524317696',
    custmorsecret = '6d8040d1b6422119a0fdc6c4ac91fea2'
    fps = [
        {
            'url': 'http://www.newtf.com/ajax/web/pages/productList',
            'ref': 'http://www.newtf.com/',
            'form': {'tplid': '5133', 'template': 'product', 'custmorsecret': custmorsecret}
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(NewtfSpider, self).__init__(limit, *args, **kwargs)

    def parse_fund(self, response):
        funds = json.loads(response.text)['data']
        for fund in funds:
            self.ips.append({
                'url': 'http://www.newtf.com/ajax/web/pages/productNetvalues',
                'ref': 'http://www.newtf.com/',
                'form': {'pid': str(fund["pid"]), 'template': 'product-det', 'monthTap': '0', 'custmorsecret': self.custmorsecret},
                'ext': {'fund_name': str(fund["product_name"])}
            })

        yield self.request_next()

    def parse_item(self, response):
        nvList = json.loads(response.text)['data']
        for eachNv in nvList:
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            ext = response.meta['ext']
            item['fund_name'] = ext['fund_name']
            init_date = eachNv['cdate']
            item['statistic_date'] = datetime.strptime(init_date, '%Y-%m-%d')
            nav = eachNv['per_netvalue']
            item['nav'] = float(nav) if nav is not None else None
            added_nav = eachNv['total_netvalue']
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item

        yield self.request_next()
