# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import Request
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhongyuInvsetSpider(GGFundNavSpider):
    name = 'FundNav_ZhongyuInvset'
    sitename = '中域投资'
    channel = '投资顾问'
    allowed_domains = ['www.shcfic.com']
    start_urls = ['http://www.shcfic.com/index.php']

    def __init__(self, *args, **kwargs):
        super(ZhongyuInvsetSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.shcfic.com/user.php?act=login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.shcfic.com/user.php?act=act_login',
                          formdata={'mobile': '13523794375',
                                    'name': '123456',
                                    'utf8': '✓',
                                    'back_act': 'http://www.shcfic.com/index.php'
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [{'url':'http://www.shcfic.com/category.php','ref':'http://www.shcfic.com/index.php'}]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath('/html/body/div[2]/div/ul/li/a/@href').extract()
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

        fund_name = response.xpath("/html/body/div[2]/div[2]/div[1]/span/text()").extract_first()
        rows = response.xpath('//*[@id="list_td"]/table/tbody/tr')
        rows.pop(0)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[1]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.xpath("./td[2]/text()").extract_first())
            item['added_nav'] = float(row.xpath("./td[3]/text()").extract_first())
            yield item

        yield self.request_next(fps, ips)
