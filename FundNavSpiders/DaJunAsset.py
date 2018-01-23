# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class DaJunAssetSpider(GGFundNavSpider):
    name = 'FundNav_DaJunAsset'
    sitename = '大钧资产'
    channel = '投资顾问'
    allowed_domains = ['www.greatwheel.com.cn']
    start_urls = ['http://www.greatwheel.com.cn/#/product?tplid=4773&id=8']
    cookies = 'pgv_pvi=462177280; pgv_si=s4667771904'

    def __init__(self, limit=None, *args, **kwargs):
        super(DaJunAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.greatwheel.com.cn/ajax/web/pages/productList?tplid=4773&template=product&custmorsecret=ab7a03053f621ed15178d844c60fb445',
                'ref': 'www.greatwheel.com.cn/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = json.loads(response.text)['data']
        for fund in funds:
            pid = fund['pid']
            product_name = fund['product_name']
            u = 'http://www.greatwheel.com.cn/#/product-det?tplid=4773&target=name&pid=' + pid
            ips.append({
                'url': 'http://www.greatwheel.com.cn/ajax/web/pages/productNetvalues?',
                'form': {'pid': pid, 'template': 'product-det', 'monthTap': '0', 'custmorsecret':'ab7a03053f621ed15178d844c60fb445'},
                'ref': u,
                'ext': {'fund_name': product_name},
            })

        yield self.request_next([], ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        datas = json.loads(response.text)['data']
        for data in datas:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = data['cdate']
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['statistic_date'] = statistic_date

            nav = data['per_netvalue']
            nav = re.search(r'([0-9.]+)', nav)
            nav = nav.group(0) if nav is not None else None
            item['nav'] = float(nav) if nav is not None else None

            added_nav = data['total_netvalue']
            added_nav = re.search(r'([0-9.]+)', added_nav)
            added_nav = added_nav.group(0) if added_nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

        yield self.request_next(fps, ips)