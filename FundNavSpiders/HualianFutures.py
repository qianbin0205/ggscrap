# -*- coding: utf-8 -*-

import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class HualianFuturesSpider(GGFundNavSpider):
    name = 'FundNav_HualianFutures'
    sitename = '华联期货'
    channel = '发行机构'
    allowed_domains = ['www.hlqh.com']
    start_urls = ['http://www.hlqh.com']

    def __init__(self, limit=None, *args, **kwargs):
        super(HualianFuturesSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cookies = 'real_ipd=203.110.179.245; UM_distinctid=160e4ad4e3d576-0b6d493255421c-393d5c04-15f900-160e4ad4e3e7ae; _cnzz_CV4130363=toJSONString%7C%7C; ECS_ID=2495a26723d6e09487b88b48bc4266ac2d607d81; ECS[display]=grid; noHint=1; td_cookie=11049320; ECS[history]=223%2C220%2C221%2C224; CNZZDATA4130363=cnzz_eid%3D295074612-1515661889-http%253A%252F%252Fwww.hlqh.com%252F%26ntime%3D1515672890'
        fps = [
            {
                'url': 'http://www.hlqh.com/product.php',
                'ref': 'http://www.hlqh.com',
                'username': 'ZYYX',
                'passowrd': 'ZYYX888',
                'cookies': cookies
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        if response.url == 'http://www.hlqh.com/product.php':
            funds = response.xpath("//div[@class='pro-table']/table/tr/td[1]/em/a/@href").extract()
            for fund in funds:
                url = urljoin(get_base_url(response), fund)
                fps.append({
                    'url': url,
                    'ref': response.url,
                })
        else:
            fund_name = response.xpath("//div[@class='projs-box1']/h5/text()").extract_first()
            id = response.url.split('=', 1)[1]
            ips.append({
                    'url': 'http://www.hlqh.com/goods.php?act=get_data&id=' + id + '&type=1',
                    'ref': response.url,
                    'headers': {
                                'X-Requested-With': 'XMLHttpRequest',
                                'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript'
                                },
                    'ext': {'fund_name': fund_name}
                })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        ext = response.meta['ext']
        fund_name = ext['fund_name']

        resp = json.loads(response.text)
        rows = resp['data']
        if rows is not None:
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.request.headers['Referer']

                item['fund_name'] = fund_name

                statistic_date = row['date']
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                added_nav = row['value']
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item

        yield self.request_next(fps, ips)
