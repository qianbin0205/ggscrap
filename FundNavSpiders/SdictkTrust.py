# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SdictkTrustSpider(GGFundNavSpider):
    name = 'FundNav_SdictkTrust'
    sitename = '国投泰康信托'
    channel = '信托净值'
    allowed_domains = ['www.sdictktrust.com']
    start_urls = []
    fps = [
        {
            'url': 'http://www.sdictktrust.com/cn/cpjz/A0227index_1.jsp',
            'ref': None,
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(SdictkTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//table[@class='jingzlist']/tbody/tr")
        for fund in funds:
            url = fund.xpath("./td[last()]/a/@href").extract_first()
            url = urljoin(get_base_url(response), url)
            fund_name = fund.xpath("./td[1]/text()").extract_first()
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund.xpath("./td[1]/text()").extract_first()
            statistic_date = fund.css('td:nth-child(3)').re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(fund.css('td:nth-child(4)::text').extract_first())
            item['added_nav'] = float(fund.css('td:nth-child(5)::text').extract_first())
            yield item

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = response.xpath("//table[@class='jingzlist']/tbody/tr")
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('td:nth-child(1)::text').extract_first().replace('\r\n\t', '').strip()
            if statistic_date == '0-13-7--20':
                yield self.request_next(fps, ips)
                return
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.css('td:nth-child(2)').re_first(r'>\s*?([0-9.]+)\s*?<')
            item['nav'] = float(nav)if nav else None

            added_nav = row.css('td:nth-child(3)').re_first(r'>\s*?([0-9.]+)\s*?<')
            item['added_nav'] = float(added_nav)if added_nav else None
            yield item

        yield self.request_next(fps, ips)


