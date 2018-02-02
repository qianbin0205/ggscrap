# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class DdqhSpider(GGFundNoticeSpider):
    name = 'FundNotice_Ddqh'
    sitename = '大地期货'
    channel = '公告'
    entry = 'http://www.ddqh.com/ziguan.php'
    allowed_domains = ['www.ddqh.com']
    start_urls = []

    lps = [
        {
            'url': 'http://www.ddqh.com/ziguan.php',
            'ref': None
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(DdqhSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        funds = response.xpath("//div[@class='playlist']/ul/li")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            url = fund.xpath("./a/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = fund.xpath("./a/text()").extract_first()
            publish_time = fund.xpath("./span/text()").re_first(r'\d+-\d+-\d+')
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath("//a[text()='»']/@href").extract_first()
        if next_url is not None and next_url != response.url:
            self.lps.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
        yield self.request_next()


