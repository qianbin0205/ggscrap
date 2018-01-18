# -*- coding: utf-8 -*-

from scrapy import Request
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import json


class QiluzqSpider(GGFundNavSpider):
    name = 'FundNav_Qiluzq'
    sitename = '齐鲁证券'
    channel = '券商资管净值'
    allowed_domains = ['www.ztzqzg.com']
    start_urls = ['https://www.ztzqzg.com/']

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'remember_me_user=13916427906; tip_advertising=1; Hm_lvt_b45288d4cb30f48df433f9ed8f380e90=1514890208,1516095935,1516159855; advertcookie=156; ql_uid=s%3AdtqmX4JuueZ3oM0LvYCmdvphtBEO66V3.GsKjEy%2B3yK3OvpRxplcfZDLmV4SMR3A81GtmUdW9k08; remember_me_company=13916427906; userType=p; userId=YJQUp%40eI9d9z9WyXSrpuH2; login=true; Hm_lpvt_b45288d4cb30f48df433f9ed8f380e90=1516170771'

    def __init__(self, limit=None, *args, **kwargs):
        super(QiluzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='https://www.ztzqzg.com/products/product-category/99/t/t',
                      meta={'fps': [], 'ips': []},
                      cookies=self.cookies,
                      callback=self.parse_fund_pre)

    def parse_fund_pre(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//div[@class='product-series-list']/ul/li/a/@data-qurl").extract()[28:]
        for url in urls:
            url = urljoin(get_base_url(response), url)
            fps.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(fps, ips)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//ul[@class='sroll-div']/li")[1:]
        for fund in funds:
            fund_name = fund.xpath('./span[@class="col-md-4"]/@data-name').extract_first()
            fund_code = fund.xpath('./span[@class="col-md-4"]/@data-fundcode').extract_first()
            ips.append({
                'url': 'https://www.ztzqzg.com/products/historyProfit',
                'form': {'fundCode': fund_code},
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        data = json.loads(response.text)['data']
        dates = data['x']
        navs = data['y1']
        addednavs = data['y2']
        extra = json.loads(response.text)['extra']
        for i in range(0, len(dates)):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = dates[i]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            if extra == 3 or extra == 2:
                nav = navs[i]
                item['nav'] = float(nav) if nav is not None else None

                added_nav = addednavs[i]
                item['added_nav'] = float(added_nav) if added_nav is not None else None
            elif extra == 1:
                income_value_per_ten_thousand = navs[i]
                item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand) if income_value_per_ten_thousand is not None else None

                d7_annualized_return = addednavs[i]
                item['d7_annualized_return'] = float(d7_annualized_return * 100)if d7_annualized_return is not None else None
            yield item

        yield self.request_next(fps, ips)
