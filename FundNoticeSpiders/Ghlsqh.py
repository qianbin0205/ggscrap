# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class GhlsqhSpider(GGFundNoticeSpider):
    name = 'FundNotice_Ghlsqh'
    sitename = '国海良时期货'
    allowed_domains = ['www.ghlsqh.com.cn']
    start_urls = []

    lps = [
        {
            'ch': {
                'name': '资管公告',
                'url_entry': 'http://www.ghlsqh.com.cn/news/list-184.html',
                'count': 0
            },
            'url': 'http://www.ghlsqh.com.cn/news/list-184.html',
            'ref': None
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(GhlsqhSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        pi = response.meta['pi']
        ch = pi['ch']
        funds = response.xpath("//ul[@class='list-ul']/li")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url_entry'] = ch['url_entry']
            url = fund.xpath("./a[1]/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = fund.xpath("./a[1]/text()").extract_first()
            publish_time = fund.xpath("./span/text()").re_first(r'\d+-\d+-\d+')
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
            ch['count'] = ch['count'] + 1
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            self.lps.append({
                'ch': ch,
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
        yield self.request_next()

