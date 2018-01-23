# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SZyuanwangjiaoSpider(GGFundNavSpider):
    name = 'FundNav_SZyuanwangjiao'
    sitename = '深圳远望角投资'
    channel = '投资顾问'
    allowed_domains = ['www.foresightamc.com']
    start_urls = ['http://www.foresightamc.com/']

    def __init__(self, limit=None, *args, **kwargs):
        super(SZyuanwangjiaoSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.foresightamc.com/',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('div.hpro.l>ul>table>tr:not(:first-child)')
        for fund in funds:
            url = fund.xpath("./td[1]/a/@href").extract_first()
            url = urljoin(get_base_url(response), url)
            fund_name = fund.xpath("./td[1]/a/text()").re_first(r'[^\（\.]+')
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund.css('td:first-child>a::text').re_first(r'[^\（\.]+')
            statistic_date = fund.css('td:nth-child(3)').re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(fund.css('td:nth-child(2)::text').extract_first())
            yield item

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = response.css('div.procs>table>tbody>tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('td:nth-child(1)::text').extract_first().replace('\r\n\t', '').strip()
            if '-' in statistic_date:
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            elif '/' in statistic_date:
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

            item['nav'] = float(row.css('td:nth-child(2)').re_first(r'>\s*?([0-9.]+)\s*?<'))
            yield item

        yield self.request_next(fps, ips)


