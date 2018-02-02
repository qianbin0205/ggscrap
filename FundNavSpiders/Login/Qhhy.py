# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class QhhySpider(GGFundNavSpider):
    name = 'FundNav_Qhhy'
    sitename = '深圳前海华英财富'
    channel = '投顾净值'
    allowed_domains = ['www.qhhy.com.cn']
    start_urls = ['http://www.qhhy.com.cn/']

    def __init__(self, limit=None, *args, **kwargs):
        super(QhhySpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.qhhy.com.cn/Home/Login',
                          formdata={
                                    'c_mobile': '13916427906',
                                    'c_password': 'ZYYXSM123',
                                    },
                          meta={
                              'handle_httpstatus_list': [302]
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.qhhy.com.cn/Product',
                'ref': 'http://www.qhhy.com.cn',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//div[@id='main']/ul/li/a")
        for fund in funds:
            product_name = fund.xpath("./@href").extract_first().rsplit('/', 1)[1]
            url = 'http://www.qhhy.com.cn/Product/ProductNetvalueList/' + product_name
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath("//div[@id='mainTitle']/text()").extract_first()
        rows = response.css('table tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = fund_name

            statistic_date = row.css('td:nth-child(1)::text').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.css('td:nth-child(2)::text').extract_first())
            item['added_nav'] = float(row.css('td:nth-child(3)::text').extract_first())

            yield item

        url = response.xpath("//a[text()='>']/@href").extract_first()
        if url is not None:
            url = urljoin(get_base_url(response), url)
            ips.insert(0, {
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)
