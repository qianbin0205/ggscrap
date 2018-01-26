# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class JinguTrustSpider(GGFundNavSpider):
    name = 'FundNav_JinguTrust'
    sitename = '金谷信托'
    channel = '发行机构'
    allowed_domains = ['www.jingutrust.com']
    start_urls = ['http://www.jingutrust.com/home/cn/index/']

    def __init__(self, limit=None, *args, **kwargs):
        super(JinguTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://www.jingutrust.com/jgxt/common/informationsProductVal.jsp?_tp_jzcp=' + str(pg),
                'ref': 'http://www.jingutrust.com/home/cn/index/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = response.meta['pg']
        url = response.meta['url']

        funds = response.xpath("//ul[@class='product_li']/li/div[1]/a")
        for fund in funds:
            fund_name = fund.xpath("./text()").extract_first()
            u = fund.xpath("./@href").extract_first()
            u = urljoin(get_base_url(response), u)
            ips.append({
                'url': u,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        totalPage = response.xpath("//a[text()='尾页']/@href").re_first(r"javascript:page\(\'jzcp\',\s*(\d+)\);")
        if totalPage is not None:
            if pg < int(totalPage):
                fps.append({
                    'pg': pg + 1,
                    'url': url,
                    'ref': response.url,

                })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = response.css('ul.info_news_list_ul>li')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('div:first-child').re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.css('div:nth-child(2)').re_first(r'>\s*?([0-9.]+)\s*?<'))
            yield item

        url = response.css('div.info_page>ul>li a').xpath('self::a[re:test(text(), "\s*下一页\s*")]/@href').extract_first()
        if url is not None and url != '#':
            url = urljoin(get_base_url(response), url)
            ips.insert(0, {
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
