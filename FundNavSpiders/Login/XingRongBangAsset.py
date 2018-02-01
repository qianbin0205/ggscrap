# -*- coding: utf-8 -*-


from datetime import datetime, date
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import re


class XingRongBangAssetSpider(GGFundNavSpider):
    name = 'FundNav_XingRongBangAsset'
    sitename = '厦门鑫融邦资产'
    channel = '投资顾问'
    allowed_domains = ['.xrbzb.icoc.me']
    start_urls = ['http://www.xrbzb.icoc.me/col.jsp?id=101']

    def __init__(self, limit=None, *args, **kwargs):
        super(XingRongBangAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.xrbzb.icoc.me/ajax/login_h.jsp',
                          formdata={'cmd': 'loginMember',
                                    'acct': 'xrb123',
                                    'pwd': '9e01d72e0d28e144c3458989c95580ee',
                                    'autoLogin': 'false',
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):
        ips = [
            {
                'url': self.start_urls[0],
                'ref': 'http://xhh.invest.ldtamp.com/',
                'ext': {'fund_name': '鑫融邦大有期货匹克辛亚7号私募'}
            }
        ]

        yield self.request_next([], ips)

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        item = GGFundNavItem()
        taget_area = response.xpath('//div[@id="images"')
        # filter = [_.xpath('//text()') for _ in taget_area]
        str_info = str(taget_area)

        # for i in str_info:
        # for i in info_list:
        #     statistic_date = i.split('：')[0]
        #     nav = i.split('：')[1]
        #     item['sitename'] = self.sitename
        #     item['channel'] = self.channel
        #     item['url'] = response.url
        #
        #     item['fund_name'] = fund_name
        #
        #     item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
        #
        #     item['nav'] = float(nav)
        #     item['added_nav'] = None
        yield item
