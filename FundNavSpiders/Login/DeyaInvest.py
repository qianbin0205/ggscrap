# -*- coding: utf-8 -*-

import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class DeyaInvestSpider(GGFundNavSpider):
    name = 'FundNav_DeyaInvest'
    sitename = '德亚投资'
    channel = '投资顾问'
    allowed_domains = ['www.deyainvest.com']
    start_urls = ['http://www.dsf.cn/dsqh/zcgl/zgcp/index.shtml']

    def __init__(self, limit=None, *args, **kwargs):
        super(DeyaInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.deyainvest.com/login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        authenticity_token = response.css('.form-login>input[name="authenticity_token"]::attr(value)').extract_first()
        yield FormRequest(url=response.url,
                          formdata={'utf8': '✓', 'commit': '登录',
                                    'session[mobile]': '13916427906',
                                    'session[password]': 'ZYYXSM123',
                                    'session[remember_me]': '1',
                                    'authenticity_token': authenticity_token},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.deyainvest.com/products',
                'ref': response.url,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        csrf_token = response.css('html head meta[name="csrf-token"]::attr(content)').extract_first()
        funds = response.css('.products>.product>.row>.content')
        for fund in funds:
            fund_name = str.strip(fund.css('.product-full-name::text').extract_first())
            url = fund.css('.nav>a::attr(href)').extract_first()
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,
                'headers': {
                    'X-CSRF-Token': csrf_token,
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

        dates = response.css('::text').re(r'date.push\(\\\'(\d+-\d+-\d+)\\\'\);')
        navs = response.css('::text').re(r'data.push\(\\\'([0-9.]+)\\\'\);')
        for i, v in enumerate(dates):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = fund_name

            statistic_date = v
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(navs[i])

            yield item

        yield self.request_next(fps, ips)
