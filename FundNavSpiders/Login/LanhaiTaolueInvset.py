# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LanhaiTaolueInvsetSpider(GGFundNavSpider):
    name = 'FundNav_LanhaiTaolue'
    sitename = '蓝海韬略'
    channel = '投资顾问'
    allowed_domains = ['www.cbs-holdings.com']
    start_urls = ['http://www.cbs-holdings.com/Index']

    def __init__(self, *args, **kwargs):
        super(LanhaiTaolueInvsetSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.cbs-holdings.com/Index/login',
                          formdata={'phone': '17839170174',
                                    'pwd_name': 'by123456',
                                    'utf8': '✓'
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [{'url':'http://www.cbs-holdings.com/sunprivate/index','ref':'http://www.cbs-holdings.com/Index'}]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath('//html/body/div[2]/div[2]/div[1]/ul/li/a/@href').extract()
        funds.pop(0)
        funds.pop(0)
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

        fund_name = response.xpath('//*[@id="fund-gy"]/div[1]/div[1]/p[1]/span/text()').extract_first()
        rows = response.xpath('//*[@id="divmodal"]/div/div/div[2]/div/div/table/tbody/tr')
        rows.pop(0)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[1]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = row.xpath("./td[2]/text()").extract_first()
            if '（已清盘）' == nav :
                continue
            item['nav'] = float(nav)
            added_nav = row.xpath("./td[3]/text()").extract_first()
            item['added_nav'] = float(added_nav)
            yield item

        yield self.request_next(fps, ips)
