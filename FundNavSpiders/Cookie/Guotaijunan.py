# -*- coding: utf-8 -*-

import time
import json
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class GuotaijunanSpider(GGFundNavSpider):
    name = 'FundNav_Guotaijunan'
    sitename = '国泰君安'
    channel = '券商资管净值'
    allowed_domains = ['www.gtjazg.com']
    start_urls = ['https://www.gtjazg.com/index.jsp']

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'gjzgs1=93258df25a7846b0f01e47621e0e11b2; showthemenr=show; shotanchuang=; login_sign=99ef2a50615f458381307844ff1ea591; s201_SESSION=95856249E43A368DB6C3740311629BF0'

    def __init__(self, limit=None, *args, **kwargs):
        super(GuotaijunanSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'https://www.gtjazg.com/jhjhPage?content_type=1&fundstate=1&qulified=2&_=' + str(round(time.time() * 1000)),
                'ref': 'https://www.gtjazg.com/producedIndex?fundstate=1&content_type=1'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//div[@class='table table-col'][position()<4]/table/tr")
        for fund in funds:
            fund_code = fund.xpath("./td[1]/text()").extract_first().strip()
            fund_name = fund.xpath("./td[2]/text()").extract_first().strip().replace('\r\n\t', '')
            ips.append({
                'url': 'https://www.gtjazg.com/fundnav/fundchart?date_condition=now&fundcode=' + fund_code +'&starttime=&endtime=&_=' + str(round(time.time() * 1000)),
                'ref': 'https://www.gtjazg.com/producedDetail?fundcode=' + fund_code + '&valueType=3',
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = json.loads(response.text)['data']['dataList']
        if rows is not None:
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name

                statistic_date = row['release_date'][0:10]
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                d7_annualized_return = row['income_ratio']
                item['d7_annualized_return'] = float(d7_annualized_return * 100) if d7_annualized_return is not None else None

                income_value_per_ten_thousand = row['income_unit']
                item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand) if income_value_per_ten_thousand is not None else None

                nav = row['net_value']
                item['nav'] = float(nav) if nav is not None else None

                added_nav = row['total_net_value']
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item

        yield self.request_next(fps, ips)
