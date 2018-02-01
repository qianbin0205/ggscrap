# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class NewCenturyFuturesSpider(GGFundNoticeSpider):
    name = 'FundNotice_NewCenturyFutures'
    sitename = '新世纪期货'
    channel = '公告'
    entry = 'http://www.zjncf.com.cn/asset-management/product-publicity'
    allowed_domains = ['www.zjncf.com.cn']
    start_urls = []

    lps = [
        {
            'pg': 0,
            'url': lambda pg: 'http://www.zjncf.com.cn/asset-management/product-publicity?pageNum=' + str(pg),
            'ref': None
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(NewCenturyFuturesSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        pi = response.meta['pi']
        pg = pi['pg']
        next_url = response.meta['url']

        funds = response.xpath('//div[@class="test-newslist"]/ul/li/a')
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry

            url = fund.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            item['url'] = url

            title = fund.xpath(r'./span[2]/text()').extract_first()
            item['title'] = title

            publish_time = fund.xpath('./span[3]/text()').re_first(r'\d+-\d+-\d+')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item['publish_time'] = publish_time
            yield item
        total_count = int(response.xpath('//div[@class="pagination"]/@data-pagecount').extract_first())
        total_pg = total_count // 15 if (total_count % 15) == 0 else total_count // 15 + 1

        if pg < total_pg - 1:
            self.lps.append({
                'pg': pg + 1,
                'url': next_url,
                'ref': response.url
            })
        yield self.request_next()
