# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class WuhanWeixinFundSpider(GGFundNavSpider):
    name = 'FundNav_WuhanWeixinFund'
    sitename = '武汉威信投资'
    channel = '投资顾问'
    allowed_domains = ['www.weixinfund.com.cn']
    start_urls = ['http://www.weixinfund.com.cn/']

    def __init__(self, limit=None, *args, **kwargs):
        super(WuhanWeixinFundSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.weixinfund.com.cn/index.php?c=content&a=show&id=29',
                'ref': None
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//div[@class='menust']/ul/li/a/@href").extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,

            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        dates = response.css('.dis>table>tbody>tr:not(:first-child)>td:first-child').re(r'\d+-\d+-\d+')
        navs = response.css('.dis>table>tbody>tr:not(:first-child)>td:nth-child(2)').re(r'>\s*?([0-9.]+?)\s*?<')
        if len(dates) > 0:
            for i in range(0, len(dates)):
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = response.xpath("//div[@class='prolist']/h1/em/text()").extract_first()

                statistic_date = dates[i]
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                item['nav'] = float(navs[i]) if navs[i] is not None else None
                yield item

        yield self.request_next(fps, ips)
