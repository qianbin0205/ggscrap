# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class AnHuiJiaHeAseetSpider(GGFundNavSpider):
    name = 'FundNav_AnHuiJiaHeAseet'
    sitename = '安徽嘉和投资'
    channel = '投顾净值'
    allowed_domains = ['www.ahjiahe.cn']
    start_urls = ['http://www.ahjiahe.cn/default.asp']

    fps = [{

        'url': 'http://www.ahjiahe.cn/info.asp?second_id=9002',
        'ref': 'http://www.ahjiahe.cn/member.asp?msg=unlogin&returnUrl=display.asp?id=1051&'
    }]

    username = 'zjz'
    password = '111111'

    def __init__(self, *args, **kwargs):
        super(AnHuiJiaHeAseetSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.ahjiahe.cn/member.asp?msg=&returnUrl=',
                          formdata={'name': 'zjz',
                                    'pass': '111111',
                                    },
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [302, 301]
                          },
                          callback=self.parse_fund)

    def parse_fund(self, response):
        href_list = response.css('div.list_news_01 li a::attr(href)').extract()
        for href in href_list:
            self.ips.append({
                'url': urljoin(get_base_url(response), href),
                'ref': response.url
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = re.sub(r'净值.*|\(.*', '', response.css('div.display_title h1::text').extract_first())
        date_list = response.xpath('//tbody[1]//tr//td[2]//text()').extract()
        filter1 = [''.join(_.split()) for _ in date_list if _.strip()][1:]
        nav_list = response.xpath('//tbody[1]//tr//td[3]//text()').extract()
        filter2 = [''.join(_.split()) for _ in nav_list if _.strip()][1:]
        added_nav_list = response.xpath('//tbody[1]//tr//td[4]//text()').extract()
        filter3 = [''.join(_.split()) for _ in added_nav_list if _.strip()][1:]

        for date, nav, added_nav in zip(filter1, filter2, filter3):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(date, '%Y%m%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

        yield self.request_next()
