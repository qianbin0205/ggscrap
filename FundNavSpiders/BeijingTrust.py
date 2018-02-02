# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class BeijingTrustSpider(GGFundNavSpider):
    name = 'FundNav_BeijingTrust'
    sitename = '北京国际信托'
    channel = '信托净值'
    allowed_domains = ['www.bjitic.com']
    start_urls = ['https://www.bjitic.com/index.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(BeijingTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'https://www.bjitic.com/sun_product.html',
                'ref': 'https://www.bjitic.com/index.html',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.css('div.newslist>table>tr>td:first-child>a::attr(href)').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath("//div[@class='money_lb']/h2/u/text()").extract_first()
        funds = response.xpath("//div[@class='qmm_lb']/table/tr")[1:]
        for fund in funds:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = fund.xpath("./td[1]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = fund.xpath("./td[2]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['nav'] = float(nav) if nav is not None else None

            added_nav = fund.xpath("./td[3]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['added_nav'] = float(added_nav)if added_nav is not None else None

            yield item

        yield self.request_next(fps, ips)
