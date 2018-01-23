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
    start_urls = ['http://www.xrzfund.com:801/(S(0mwyuz55eeqjyfb315b2zkb5))/login.aspx?type=out']

    def __init__(self, limit=None, *args, **kwargs):
        super(XrzFundSpider, self).__init__(limit, *args, **kwargs)

    def parse(self, response):
        __VIEWSTATE = response.xpath(".//input[@name='__VIEWSTATE']/@value").extract_first()
        __EVENTVALIDATION = response.xpath(".//input[@name='__EVENTVALIDATION']/@value").extract_first()
        yield FormRequest(url='http://www.xrzfund.com:801/(S(0mwyuz55eeqjyfb315b2zkb5))/login.aspx?type=out',
                          formdata={'__VIEWSTATE': __VIEWSTATE,
                                    '__EVENTVALIDATION': __EVENTVALIDATION,
                                    'username': '123',
                                    'password': '123456',
                                    'BtnLogin': '立即登录',
                                    're_check': '1',
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):

        fps = [
            {
                'url': 'http://www.xrzfund.com:801/(S(4hbebdpxir5zunwywfgp4w5k))/chanpinxinxi.aspx?type=%E4%BB%99%E4%BA%BA%E6%8E%8C%E9%87%91%E7%89%9B1%E5%8F%B7%E5%9F%BA%E9%87%91',
                'ref': 'http://www.xrzfund.com:801/(S(4hbebdpxir5zunwywfgp4w5k))/Index.aspx',
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

            item['nav'] = float(row.xpath("./td[3]/text()").extract_first())
            item['added_nav'] = float(row.xpath("./td[4]/text()").extract_first())

            yield item

        yield self.request_next(fps, ips)
