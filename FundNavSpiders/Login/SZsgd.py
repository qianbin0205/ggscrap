# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
import random
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import json


class SZsgdSpider(GGFundNavSpider):
    name = 'FundNav_SZsgd'
    sitename = '深圳盛冠达资产投资'
    channel = '投顾净值'
    allowed_domains = ['www.sz-sgd.com']
    start_urls = []
    username = 18602199319
    password = 'yadan0319'

    def __init__(self, limit=None, *args, **kwargs):
        super(SZsgdSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.sz-sgd.com/User.ashx?r='+str(random.random())+'&type=login&username=18602199319&password=yadan0319', callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.sz-sgd.com/Product.aspx',
                'ref': None,

            }
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//ul[@class='fund_li']/li/div[@class='fund_name']/h3/a")
        for fund in funds:
            fund_name = fund.xpath("./text()").extract_first()
            url = fund.xpath("./@href").extract_first()
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        datas = response.css('::text').re_first(r'var\s*report\s*=\s*\"(.*?)\";')
        rows = json.loads(datas.replace('\\', ''))
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = str(row['y'])+str(row['m'])+str(row['d'])
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')

            nav = row['n']
            item['nav'] = float(nav)if nav is not None else None

            added_nav = row['t']
            item['added_nav'] = item['nav'] = float(added_nav)if added_nav is not None else None

            yield item

        yield self.request_next(fps, ips)
