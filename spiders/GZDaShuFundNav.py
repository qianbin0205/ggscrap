# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class GZDaShuFundNavSpider(GGFundNavSpider):
    name = 'GZDaShuFundNav'
    sitename = '广州大树投资'
    allowed_domains = ['www.gzdashu.com']
    start_urls = ['http://www.gzdashu.com/cpzx.aspx']

    def __init__(self, limit=None, *args, **kwargs):
        super(GZDaShuFundNavSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.gzdashu.com/cpzx.aspx',
                'ref': 'http://www.gzdashu.com/',
                'cookies': 'ASP.NET_SessionId=kjkteiec1qmis0rzrsthohun; td_cookie=11049074'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath(r'//a[re:test(@id, "^qxcp[0-9]+$")]')
        for fund in funds:
            url = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        rows = response.css('table.mychat tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = row.css('td:nth-child(1)::text').extract_first()
            item['nav'] = row.css('td:nth-child(2)::text').extract_first()
            item['added_nav'] = row.css('td:nth-child(3)::text').extract_first()
            item['statistic_date'] = row.css('td:nth-child(4)::text').extract_first()
            yield item

        yield self.request_next(fps, ips)
