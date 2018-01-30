# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class XinshunCapitalSpider(GGFundNoticeSpider):
    name = 'FundNotice_XinshunCapital'
    sitename = '北京鑫顺和康投资'
    allowed_domains = ['www.xinshuncapital.com']
    start_urls = []

    lps = [
        {
            'ch': {
                'name': '新闻资讯-公司公告',
                'url_entry': 'http://www.xinshuncapital.com/?c=news&catid=6',
                'count': 0
            },
            'url': 'http://www.xinshuncapital.com/?c=news&catid=6',
            'ref': None
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(XinshunCapitalSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        ch = response.meta['ch']
        funds = response.xpath("//div[@class='new']/ul/li")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url_entry'] = ch['url_entry']
            url = fund.xpath("./span/a/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = fund.xpath("./span/a/text()").extract_first()
            publish_time = fund.xpath("./text()").re_first(r'\d+-\d+-\d+')
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
            ch['count'] = ch['count'] + 1
        url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if url is not None:
            self.lps.append({
                'ch': ch,
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })
        yield self.request_next()


