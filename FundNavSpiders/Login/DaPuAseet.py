# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import FormRequest, Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class DaPuAseetSpider(GGFundNavSpider):
    name = 'FundNav_DaPuAseet'
    sitename = '大朴资产'
    channel = '投顾净值'
    allowed_domains = ['www.dapufund.com']
    start_urls = ['http://www.dapufund.com/']
    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.dapufund.com/Products',
        'ref': 'http://www.dapufund.com/Member/product'
    }]

    def __init__(self, *args, **kwargs):
        super(DaPuAseetSpider, self).__init__(*args, **kwargs)

    def pre_log_in(self):
        yield Request(url='http://www.dapufund.com/',
                      callback=self.log_in)

    def log_in(self, response):
        cms = response.xpath('//input[@name="__cmsform__"]/@value').extract_first()
        yield FormRequest(url='http://www.dapufund.com/Public/checkLogins',
                          formdata={'name': '13916427906',
                                    'pass': 'ZYYXSM123',
                                    '__cmsform__': cms},
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [302, 301]
                          },
                          callback=self.start_requests)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        href_list = response.css('div.sub_menu a::attr(href)').extract()
        for href in href_list:
            pid = href.split('/')[-1]
            self.ips.append({
                'url': 'http://www.dapufund.com/Products/listmore',
                'ref': response.url,
                'form': {
                    'page': '1',
                    'pid': pid
                },
                'pg': 1
            })
        yield self.request_next()

    def parse_item(self, response):
        rows = response.css('tr')
        if rows:
            for r in rows:
                row = r.css('td ::text').extract()
                fund_name = row[0]
                nav = row[1]
                added_nav = row[2]
                statistic_date = re.sub('[/.]', '-', row[3])

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(nav) if added_nav is not None else None

                yield item

            next_pg = response.meta['pg'] + 1
            self.ips.append({
                'url': 'http://www.dapufund.com/Products/listmore',
                'ref': response.url,
                'form': {
                    'page': str(next_pg),
                    'pid': response.meta['form']['pid']
                },
                'pg': next_pg
            })

        yield self.request_next()
