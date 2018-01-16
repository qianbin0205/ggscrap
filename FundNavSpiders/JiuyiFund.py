# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class JiuyiFundSpider(GGFundNavSpider):
    name = 'FundNav_JiuyiFund'
    sitename = '玖逸投资'
    channel = '投资顾问'
    allowed_domains = ['www.jiuyifund.com']
    start_urls = ['http://www.jiuyifund.com/']

    def __init__(self, limit=None, *args, **kwargs):
        super(JiuyiFundSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.jiuyifund.com/Article/news_more.asp?lmid=211',
                'ref': 'http://www.jiuyifund.com/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//div[contains(@id,'List')]/table[4]/tr/td/span/a/@href").extract()
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
        fund_name = response.xpath("//div[@class='lm_align']").re_first(r'您所在的位置(\S+)产品净值')
        fund_name = fund_name.replace(">>", '')
        rows = response.xpath("//table[@class='MsoNormalTable']/tbody/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('td:first-child').re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.css('td:nth-child(2)').re_first('>\s*?([0-9.]+?)\s*?<'))

            yield item

        yield self.request_next(fps, ips)
