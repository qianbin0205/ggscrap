# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class BjfqtzSpider(GGFundNoticeSpider):
    name = 'FundNotice_Bjfqtz'
    sitename = '蜂雀投资'
    channel = '公告'
    entry = 'http://www.bjfqtz.com/news.aspx?ParentId=5&CateId=22'
    allowed_domains = ['www.bjfqtz.com']
    start_urls = []

    lps = [
        {
            'pg': 1,
            'url': lambda pg: 'http://www.bjfqtz.com/newslist.aspx?ParentId=5&CateId=22&page=' + str(pg),
            'ref': None
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(BjfqtzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        pi = response.meta['pi']
        ch = pi['ch']
        pg = pi['pg']
        url = response.meta['url']

        funds = response.xpath("//li")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url_entry'] = ch['url_entry']
            u = fund.xpath("./div/a[2]/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), u)
            item['title'] = fund.xpath("./div/a[2]/text()").extract_first()
            publish_time = fund.xpath("./div/p").re_first(r'\d+-\d+-\d+')
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tpg = response.xpath("//span[@id='DcmsPage_PageInfo']/text()").re_first(r'(\d+)\|\d+')
        if pg < int(tpg):
            self.lps.append({
                'ch': ch,
                'pg': pg + 1,
                'url': url,
                'ref': response.url
            })
        yield self.request_next()


