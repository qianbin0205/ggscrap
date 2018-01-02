# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class Jiuxi168Spider(GGFundNavSpider):
    name = 'FundNav_Jiuxi168'
    sitename = '九溪资产'
    channel = '投资顾问'
    allowed_domains = ['www.jiuxi168.com']
    start_urls = ['http://www.jiuxi168.com/product/']

    def __init__(self, limit=None, *args, **kwargs):
        super(Jiuxi168Spider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.jiuxi168.com/product/',
                'ref': None
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css(r'.content1 li.li-list').xpath(r'descendant::a[re:test(@href, "[?&]id=\d+")]')
        for fund in funds:
            url = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
            fund_name = fund.css('::text').extract_first()
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

        fund_name = ext['fund_name']

        rows = response.css('.content2>li>table>tbody>tr')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('td:first-child').re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.css('td:nth-child(2)').re_first('>\s*?([0-9.]+?)\s*?<'))
            item['added_nav'] = float(row.css('td:nth-child(3)').re_first('>\s*?([0-9.]+?)\s*?<'))
            yield item

        url = response.css('.content2 .fylj>a.a2::attr(href)').extract_first()
        if url is not None:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
