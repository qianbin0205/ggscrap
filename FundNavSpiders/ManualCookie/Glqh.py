# -*- coding: utf-8 -*-

import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class GlqhSpider(GGFundNavSpider):
    name = 'FundNav_Glqh'
    sitename = '国联期货'
    channel = '发行机构'
    allowed_domains = ['www.glqh.com']
    start_urls = ['http://www.glqh.com/zcgljzplyxz.htm']

    def __init__(self, limit=None, *args, **kwargs):
        super(GlqhSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.glqh.com/zcgljzplyxz.htm',
                'ref': 'http://www.glqh.com/',
                'username': '15838535216',
                'password': '050835',
                'cookies': 'td_cookie=11049128; _glqh_=xDKxicFmNZ; UM_distinctid=1609b8b0b8a34e-0c27bab557c9df-5f19331c-1aeaa0-1609b8b0b8b96a; td_cookie=11049067; CNZZDATA1256302135=895841349-1514433905-http%253A%252F%252Fwww.glqh.com%252F%7C1515372378; JSESSIONID=F8417E0E8250D5AC689A52B9B443258E'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.css(r'td>p>a').xpath(r'self::a[re:test(text(), "^\s*详情\s*$")]/@href').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            fps.append({
                'url': url,
                'ref': response.url
            })

        fund = response.css('.c1-body .f-left>a[title]')
        if len(fund) >= 1:
            fund_name = fund[0].css('::attr(title)').extract_first()
            url = urljoin(get_base_url(response), fund[0].css('::attr(href)').extract_first())
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        rows = response.css('.pbox tr:not(:first-child)')
        for row in rows:
            statistic_date = row.css('td:first-child').re_first('\d+年\D*\d+月\d+日')
            if statistic_date is not None:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = ext['fund_name']

                statistic_date = re.sub('(\d+年)\D*(\d+月\d+日)', r'\1\2', statistic_date)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')

                item['added_nav'] = float(row.css('td:nth-child(2)').re_first('>\s*?([0-9.]+?)\s*?<'))
                yield item

        yield self.request_next(fps, ips)
