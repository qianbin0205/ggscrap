# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
from scrapy import Request
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class TengBeiErAssetSpider(GGFundNavSpider):
    name = 'FundNav_TengBeiErAsset'
    sitename = '成都腾倍尔资产'
    channel = '投顾净值'
    allowed_domains = ['http://www.cdtbg.com']
    start_urls = ['http://www.cdtbg.com/list-33-1.html']
    fps = []

    def __init__(self, *args, **kwargs):
        super(TengBeiErAssetSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url=self.start_urls[0],
                      callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        product_urls = response.css('tr.tts a::attr(href)').extract()
        for pro_url in product_urls:
            self.fps.append({
                'url': pro_url,
                'ref': response.url
            })
        yield self.request_next()

    def parse_fund(self, response):
        ips = response.meta['ips']
        nav_url = response.xpath('//a[contains(text(),"净值查询")]/@href').extract_first()
        ips.append({
            'url': nav_url,
            'ref': response.url
        })
        yield self.request_next()

    def parse_item(self, response):
        ips = response.meta['ips']
        rows = response.css('tr.tts')
        if rows:
            for row in rows:
                fund_name = row.xpath('./td[@width="126"]/text()').extract_first()
                statistic_date = row.xpath('./td[@width="89"]/text()').extract_first()
                nav = row.xpath('./td[@width="73"]/text()').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date,
                                                           '%Y-%m-%d') if statistic_date is not None else None
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = None
                yield item

                url = response.url
                pg = re.compile('.*-(\d+)\.html').findall(url)[0]
                sub_str = str(int(pg) + 1) + '.html'
                next_url = re.sub('\d+\.html', sub_str, url)
                ips.append(
                    {
                        'url': next_url,
                        'ref': url
                    }
                )

                yield self.request_next()
