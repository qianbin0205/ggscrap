# -*- coding: utf-8 -*-

import re
import json
from urllib.parse import urljoin
from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class XingJuInvestSpider(GGFundNavSpider):
    name = 'FundNav_XingJuInvest'
    sitename = '兴聚投资'
    channel = '投顾净值'
    allowed_domains = ['www.blossomfund.com.cn']

    username = '13916427906'
    password = '123456'
    start_urls = ['http://www.blossomfund.com.cn/label/member/login.aspx']

    fps = [{
        'url': 'http://www.blossomfund.com.cn/jjjz/list_21_cid_14.html'
    }]

    def __init__(self, *args, **kwargs):
        super(XingJuInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0],
                          formdata={
                              'loginname': '13916427906',
                              'password': '123456'
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        href_list = response.css('div.i_left a::attr(href)').extract()
        for href in href_list:
            nav_url = urljoin(response.url, href)
            self.ips.append({
                'url': nav_url
            })
        yield self.request_next()

    def parse_item(self, response):
        rows = response.css('tbody.list')[-1].css('tr')

        for row in rows:
            row_info = row.xpath('td//text()').extract()
            fund_name = row_info[0]
            statistic_date = row_info[2]
            nav = float(row_info[4])
            add_nav = float(row_info[5])
            if '中信兴聚一期' in fund_name:
                # 如果产品为“中信兴聚一期”所有净值需除以100
                nav = nav / 100
                add_nav = add_nav / 100

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = nav
            item['added_nav'] = add_nav
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        yield self.request_next()
