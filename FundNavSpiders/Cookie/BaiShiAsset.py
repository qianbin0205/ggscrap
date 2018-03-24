# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class BaiShiAssetSpider(GGFundNavSpider):
    name = 'FundNav_BaiShiAsset'
    sitename = '白石资产'
    channel = '投资顾问' #需求文档未写明
    allowed_domains = ['www.whiterock.cn']
    start_urls = ['http://www.whiterock.cn/index.php']

    username = '朵朵'
    password = 'bs123456'
    cookies = 'PHPSESSID=l38fjniv0jem4eejhq5qbs2av5; reads=1'

    def __init__(self, *args, **kwargs):
        super(BaiShiAssetSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fps = [{
            'url': 'http://www.whiterock.cn/index.php'
        }]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        ips = response.meta['ips']

        funds = response.css('select#select option')
        for fund in funds:
            api_key = fund.css('::attr(value)').extract_first()
            fund_name = fund.css('::text').extract_first()

            ips.append({
                'url': 'http://www.whiterock.cn/_api.php',
                'ref': response.url,
                'form': {
                    'id': api_key,
                    'type': '6'
                },
                'ext': {
                    'fund_name': fund_name
                }
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.css('table tr')
        for row in rows:
            td_text = row.css('td::text').extract_first()
            if '日期' in td_text:
                continue
            statistic_date = row.css('td::text').extract_first()
            nav = row.css('td span::text').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = None
            yield item

        yield self.request_next()
