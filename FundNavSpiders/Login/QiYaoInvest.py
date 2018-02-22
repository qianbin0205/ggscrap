# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin

from scrapy import FormRequest
from scrapy import Request
from scrapy.utils.response import get_base_url

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class QiYaoInvestSpider(GGFundNavSpider):
    name = 'FundNav_QiYaoInvest'
    sitename = '上海七曜投资'
    channel = '投资顾问'
    allowed_domains = ['www.qiyaoinvest.com']
    start_urls = ['http://www.qiyaoinvest.com/']

    def __init__(self, *args, **kwargs):
        super(QiYaoInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.qiyaoinvest.com/pc/login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        yield FormRequest(url='http://www.qiyaoinvest.com/pc/login/submit_user',
                          formdata={
                              'utf8': '✓',
                              'authenticity_token': authenticity_token,
                              'login_name': '13916427906',
                              'password': 'ZYYXSM123',
                              'auto_login': 'on',
                              'login': '0'
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.qiyaoinvest.com/pc/profit/all',
                'ref': response.url
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = response.xpath('//a[@class="top_xq_01"]/@href').extract()
        for fund in funds:
            url = urljoin(get_base_url(response), fund)
            ips.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath('//table[@class="table_k"]/tbody/tr[1]/td[@class=" wid11_1"]/text()').extract_first()
        rows = response.xpath('//div[@id="nets"]/table[@class="table_k"]/tbody/tr')[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = fund_name
            statistic_date = row.xpath("./td[1]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = row.xpath("./td[2]/text()").extract_first()
            item['nav'] = float(nav)
            added_nav = row.xpath("./td[3]/text()").extract_first()
            item['added_nav'] = float(added_nav)

            yield item
        yield self.request_next(fps, ips)
