# -*- coding: utf-8 -*-

import config
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhejiangHuianInvsetSpider(GGFundNavSpider):
    name = 'FundNav_ZhejiangHuian'
    sitename = '浙江慧安家族财富投资'
    channel = '投资顾问'
    allowed_domains = ['www.huianwealth.com']
    start_urls = ['http://www.huianwealth.com/wzsy']

    def __init__(self, *args, **kwargs):
        super(ZhejiangHuianInvsetSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.huianwealth.com/hydl', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.huianwealth.com/userlogin?returnurl=',
                          formdata={'Username': '441819121@qq.com',
                                    'Password': '123456',
                                    'utf8': '✓'
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield Request(url='http://www.huianwealth.com/cpgy', callback=self.parse_fund_pre)

    def parse_fund_pre(self,response):
        fps = [{'url': 'http://www.huianwealth.com/cpjz', 'ref': response.url}]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath('//*[@id="view_list_7_277192661"]/div/ul/li[1]/div/a/@href').extract()
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

        fund_name = response.xpath('//*[@id="view_text_24_10_txt"]/div/p/span/strong/text()').extract_first()
        rows = response.xpath('//*[@id="view_text_17_10_txt"]/div/table/tbody/tr')
        rows.pop(0)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            #//*[@id="view_text_17_10_txt"]/div/table/tbody/tr[2]/td[1]/span[1]
            statistic_date = row.xpath("./td[1]/span[1]/text()").extract_first()
            statistic_date += row.xpath("./td[1]/span[2]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')

            item['nav'] = float(row.xpath("./td[2]/span[1]/text()").extract_first())
            item['added_nav'] = float(row.xpath("./td[3]/span[1]/text()").extract_first())
            yield item

        yield self.request_next(fps, ips)
