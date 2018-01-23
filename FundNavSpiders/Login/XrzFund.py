# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class XrzFundSpider(GGFundNavSpider):
    name = 'FundNav_XrzFund'
    sitename = '上海仙人掌资产'
    channel = '投资顾问'
    allowed_domains = ['www.xrzfund.com']
    start_urls = ['http://www.xrzfund.com:801/(S(iejkughmniucwrq1cejr3fho))/login.aspx?type=out']

    def __init__(self, limit=None, *args, **kwargs):
        super(XrzFundSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.xrzfund.com:801/(S(iejkughmniucwrq1cejr3fho))/login.aspx?type=out',
                          formdata={'__VIEWSTATE': '/wEPDwULLTE3MjQxODQ4MDhkZEPTBqtHxugtelWaL0YNDSgklllL6jUtq+JXcPUa+LnN',
                                    '__EVENTVALIDATION': '/wEdAAIin2PQEFVOkEdFCGEfnKzyQiUagUcDcu68gyetszRkSUveFZLSSGwlE4Efgj3cuNmZn2pg6GsvdZHkBXsjUlNa',
                                    'username': '123',
                                    'password': '123456',
                                    'BtnLogin': '立即登录',
                                    're_check': '1',
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):
        url = urljoin(get_base_url(response), 'chanpinxinxi.aspx?type=仙人掌金牛1号基金')
        fps = [
            {
                'url': url,
                'ref': urljoin(get_base_url(response), 'index.aspx'),

            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.css('div.m1>dl>dd>a::attr(href)').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = response.xpath("//div[@class='content_tab']/table/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = row.xpath("./td[1]/text()").extract_first()

            statistic_date = row.xpath("./td[2]/text()").re_first(r'\d+/\d+/\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

            nav = row.xpath("./td[3]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['nav'] = float(nav)if nav is not None else None

            added_nav = row.xpath("./td[4]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['added_nav'] = item['nav'] = float(added_nav)if added_nav is not None else None

            yield item

        yield self.request_next(fps, ips)
