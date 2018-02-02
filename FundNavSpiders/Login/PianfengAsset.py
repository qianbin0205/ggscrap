# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class PianfengAssetSpider(GGFundNavSpider):
    name = 'FundNav_PianfengAsset'
    sitename = '偏锋投资'
    channel = '投顾净值'
    allowed_domains = ['www.shpfic.com']

    start_urls = []
    fps = [
        {
            'url': 'http://www.shpfic.com/index/product/product.html',
            'ref': 'http://www.shpfic.com/index/index/index_show.html',
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(PianfengAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.shpfic.com/', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        token = response.xpath("//input[@name='__token__']/@value").extract_first()
        yield FormRequest(url='http://www.shpfic.com/index/login/login.html',
                          formdata={'username': 'BY123456',
                                    'password': 'BY123456',
                                    'option': 'login',
                                    '__token__': token,
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//table[@class='itsProduct']/tr")
        for fund in funds:
            url = fund.xpath("./td[3]/input/@onclick").re_first(r'window.open\(\'(\S+)\'\)')
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath("//table[@class='productDetail']/tr[2]/td[2]/text()").extract_first()
        rows = response.css('.right>table>tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = fund_name

            statistic_date = row.css('td:first-child').re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.css('td:nth-child(2)').re_first(r'>\s*?([0-9.]+)\s*?<'))
            item['added_nav'] = float(row.css('td:nth-child(3)').re_first(r'>\s*?([0-9.]+)\s*?<'))
            yield item
        next_url = response.xpath("//a[text()='»']/@href").extract_first()
        if next_url is not None:
            url = urljoin(get_base_url(response), next_url)
            ips.insert(0, {
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)
