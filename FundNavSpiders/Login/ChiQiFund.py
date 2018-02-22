# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin

from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ChiQiFundSpider(GGFundNavSpider):
    name = 'FundNav_ChiQiFund'
    sitename = '赤祺资产'
    channel = '投顾净值'
    allowed_domains = ['www.chiqifund.com']

    username = '13916427906'
    password = 'ZYYXSM123'

    def __init__(self, *args, **kwargs):
        super(ChiQiFundSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.chiqifund.com/login', callback=self.pars_pre_login)

    def pars_pre_login(self, response):
        csrfmiddlewaretoken = response.xpath('//input[@name="csrfmiddlewaretoken"]/@value').extract_first()
        yield FormRequest(url='http://www.chiqifund.com/login',
                          formdata={
                              'csrfmiddlewaretoken': csrfmiddlewaretoken,
                              'username': self.username,
                              'password': self.password
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [{
            'url': 'http://www.chiqifund.com/product',
            'ref': response.url
        }]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        urls = response.xpath('//div[@id="about_left"]/ul/li/a/@href').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            print(url)
            ips.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        rows = response.xpath('//div[@id="history"]/table/tr')[2:]
        for row in rows:
            fund_name = row.xpath(r'./td[1]/text()').extract_first()
            nav = row.xpath(r'./td[2]/text()').extract_first()
            added_nav = row.xpath(r'./td[3]/text()').extract_first()
            statistic_date = row.xpath("./td[4]/text()").extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
        yield self.request_next(fps, ips)
