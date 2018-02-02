# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class PingAnDaHuaSpider(GGFundNoticeSpider):
    name = 'FundNotice_PingAnDaHua'
    sitename = '平安大华汇通财富'
    allowed_domains = ['fund.pingan.com']
    start_urls = ['http://fund.pingan.com/main/index.shtml']

    def __init__(self, limit=None, *args, **kwargs):
        super(PingAnDaHuaSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        self.lps.append({
                'ch': {
                    'name': '平安大华汇通财富',
                    'url_entry': 'http://fund.pingan.com/main/index.shtml',
                    'count': 0
                },
                'url': 'http://fund.pingan.com/main/infoPublish/index.shtml',
                'ref': 'http://fund.pingan.com'
            })
        yield self.request_next()

    def parse_list(self, response):
        self.ips.append({
            'url': 'http://fund.pingan.com/servlet/json?funcNo=520004&numPerPage=8&catalogId=502&searchKey=&isChild=1&isDate=1&pageNum=1',
            'ref': response.url,
            'pg': 1
        })
        yield self.request_next()

    def parse_item(self, response):
        pi = response.meta['pi']
        pg = pi['pg']
        results = json.loads(response.text)['results']
        tpg = results[0]['totalPages']
        for result in results:
            years = result['data']
            for yeardata in years:
                datas = json.loads(yeardata['subList'])
                for data in datas:
                    name = data['name']
                    if '专户理财' == name:
                        item = GGFundNoticeItem()
                        item['sitename'] = self.sitename
                        item['channel'] = self.channel
                        item['url'] = urljoin(get_base_url(response), data['url'])
                        item['url_entry'] = response.url
                        item['title'] = data['title']
                        publish_time = data['create_date']
                        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                        yield item
        if pg < int(tpg):
            self.ips.append({
                'pg': pg + 1,
                'url': 'http://fund.pingan.com/servlet/json?funcNo=520004&numPerPage=8&catalogId=502&searchKey=&isChild=1&isDate=1&pageNum=' + str(pg),
                'ref': response.url
            })
        yield self.request_next()
