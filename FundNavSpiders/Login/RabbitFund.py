# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class RabbitFundSpider(GGFundNavSpider):
    name = 'FundNav_RabbitFund'
    sitename = '中欧瑞博'
    channel = '投资顾问'
    allowed_domains = ['www.rabbitfund.com.cn']
    start_urls = ['http://www.rabbitfund.com.cn/cn/']

    def __init__(self, limit=None, *args, **kwargs):
        super(RabbitFundSpider, self).__init__(limit, *args, **kwargs)

    def parse(self, response):
        yield FormRequest(url='http://www.rabbitfund.com.cn/cn/tools/ajax.ashx',
                          formdata={'UserName': '13916427906',
                                    'Password': 'ZYYXSM123',
                                    'Cby': '1',
                                    'Token': '',
                                    'Mod': 'Login'},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.rabbitfund.com.cn/cn/products.html',
                'ref': 'http://www.rabbitfund.com.cn/cn/member/',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//div[@class='pro-scroll']/table/tr")[1:-1]
        for fund in funds:
            url = fund.xpath("./td[1]/a/@href").extract_first()
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url is not None:
            next_url = urljoin(get_base_url(response), next_url)
            fps.append({
                'url': next_url,
                'ref': response.url,
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath("//div[@class='det-data']/h2/text()").extract_first()
        rows = response.css('.pro-det-worth>table>tr:not(:first-child)')
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

        yield self.request_next(fps, ips)
