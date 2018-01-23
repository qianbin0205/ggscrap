# -*- coding: utf-8 -*-

from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class GuangdaBankSpider(GGFundNavSpider):
    name = 'FundNav_GuangdaBank'
    sitename = '光大银行'
    channel = '投顾净值'
    allowed_domains = ['www.cebbank.com']
    start_urls = ['']

    def __init__(self, limit=None, *args, **kwargs):
        super(GuangdaBankSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        ips = [
            {
                'url': 'http://www.cebbank.com/site/gryw/yglc/lccp8/zcgllcp/ty87/yzgg73/673370/index.html',
                'ref': None,
                'ext': {'fund_name': '阳光私募基金宝'}
            },
            {
                'url': 'http://www.cebbank.com/site/gryw/yglc/lccp8/zcgllcp/ty87/yzgg73/673370/index.html',
                'ref': None,
                'ext': {'fund_name': '同赢五号2'}
            },
            {
                'url': 'http://www.cebbank.com/site/gryw/yglc/lccp8/zcgllcp/ty87/yzgg73/673370/index.html',
                'ref': None,
                'ext': {'fund_name': '同享二号'}
            },
            {
                'url': 'http://www.cebbank.com/site/gryw/yglc/lccp8/zcgllcp/ty87/yzgg73/673370/index.html',
                'ref': None,
                'ext': {'fund_name': '稳健一号'}
            },
            {
                'url': 'http://www.cebbank.com/site/gryw/yglc/lccp8/zcgllcp/ty87/yzgg73/673370/index.html',
                'ref': None,
                'ext': {'fund_name': '集优量化组合投资'}
            }
        ]

        yield self.request_next([], ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = response.xpath("//div[@class='xilan_con']/table/tbody/tr")[2:]
        for row in rows:
            if row.xpath("./td[1]/p/text()").extract_first() is not None:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                statistic_date = row.css('td:nth-child(1)>p').re_first(r'\d+-\d+-\d+')
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date is not None else None
                if fund_name == '阳光私募基金宝':
                    nav = row.css(r'td:nth-child(2)>p').re_first(r'>\s*?([0-9.]+)\s*?<')
                    item['nav'] = float(nav) if nav is not None else None

                elif fund_name == '同赢五号2':
                    nav = row.css(r'td:nth-child(3)>p').re_first(r'>\s*?([0-9.]+)\s*?<')
                    item['nav'] = float(nav) if nav is not None else None

                elif fund_name == '同享二号':
                    nav = row.css(r'td:nth-child(4)>p').re_first(r'>\s*?([0-9.]+)\s*?<')
                    item['nav'] = float(nav) if nav is not None else None

                elif fund_name == '稳健一号':
                    nav = row.css(r'td:nth-child(6)>p').re_first(r'>\s*?([0-9.]+)\s*?<')
                    item['nav'] = float(nav) if nav is not None else None

                    added_nav = row.css('td:nth-child(7)>p').re_first(r'>\s*?([0-9.]+)\s*?<')
                    item['added_nav'] = float(added_nav) if added_nav is not None else None

                elif fund_name == '集优量化组合投资':
                    nav = row.css(r'td:last-child>p').re_first(r'>\s*?([0-9.]+)\s*?<')
                    item['nav'] = float(nav) if nav is not None else None

                yield item

        yield self.request_next(fps, ips)


