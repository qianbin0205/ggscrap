# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HouChongInvestSpider(GGFundNavSpider):
    name = 'FundNav_houhonginvest'
    sitename = '上海厚崇资产'
    channel = '投资顾问'
    allowed_domains = ['www.thudamc.com']
    start_urls = ['http://www.thudamc.com/']

    def __init__(self, *args, **kwargs):
        super(HouChongInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.thudamc.com/index.php?m=content&c=index&a=lists&catid=11',
                'ref': 'https://www.thudamc.com'
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        urls = response.xpath('/html/body/div[6]/div[1]/div')
        next_url = response.xpath('//*[@id="pages"]/a[10]/@href').extract_first()
        for url in urls:
            fund_name = url.xpath('./p[1]/text()').extract_first()
            url = url.xpath('./p[2]/a/@href').extract_first()
            if fund_name is not None and fund_name.find('基金净值报告')>0:
                ips.append({
                    'url': url,
                    'ref': response.url
                })
        next_url = urljoin(get_base_url(response), next_url)
        if response.url != next_url:
            fps.append({'url': next_url, 'ref': response.url})
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        fund_name = response.xpath('/html/body/div[6]/div/table/tbody/tr[1]/td[2]/text()').extract_first()
        statistic_date = response.xpath('/html/body/div[6]/div/table/tbody/tr[9]/td[1]/text()').re_first(r'\d+')
        nav = response.xpath('//html/body/div[6]/div/table/tbody/tr[9]/td[2]/text()').extract_first()
        added_nav = response.xpath('/html/body/div[6]/div/table/tbody/tr[10]/td[2]/text()').extract_first()

        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_name
        statistic_date = datetime.strptime(statistic_date, '%Y%m%d')
        item['statistic_date'] = statistic_date
        item['nav'] = float(nav) if nav is not None else None
        item['added_nav'] = float(added_nav) if added_nav is not None else None
        yield item

        yield self.request_next(fps, ips)
