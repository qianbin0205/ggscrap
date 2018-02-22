# -*- coding: utf-8 -*-
from datetime import datetime

from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class ZczyInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZczyInvest'
    sitename = '厦门致诚卓远投资'
    channel = '投资顾问'
    allowed_domains = ['www.zczyfund.com']
    start_urls = ['http://www.zczyfund.com/index.asp']

    username = '赵赵'
    password = '123456'
    cookies = 'ASPSESSIONIDQCCSDACB=MPLFFACBNNPPHEFLGEDABLFE; ASPSESSIONIDQADRBACC=ILFPGFDBMFIOLFIPLNBMGDAF'

    def __init__(self, *args, **kwargs):
        super(ZczyInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.zczyfund.com/product01.asp',
                'ref': None
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = response.xpath(r'//table/tr[3]/td[1]/table/tr/td')[3:]
        for fund in funds:
            fund_name = fund.xpath(r'./a/text()').extract_first()
            url = fund.xpath(r'./a/@href').extract_first()
            if fund_name is None:
                fund_name = fund.xpath(r'./div/a/text()').extract_first()
                url = fund.xpath(r'./div/a/@href').extract_first()
            if fund_name is None:
                continue
            ips.append({
                'url': 'http://www.zczyfund.com/' + url,
                'ref': response.url,
                'ext': fund_name
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.meta['ext']
        rows = response.xpath(r'//table/tr[3]/td[2]/table[2]/tr')[2:]
        for row in rows:
            statistic_date = row.xpath(r'./td[1]/text()').re_first(r'\d+/\d+/\d+')
            statistic_date = datetime.strptime(statistic_date, '%Y/%m/%d')
            nav = row.xpath(r'./td[2]/text()').re_first(r'[0-9.]+')
            added_nav = row.xpath(r'./td[3]/text()').re_first(r'[0-9.]+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = statistic_date
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item
        yield self.request_next(fps, ips)
