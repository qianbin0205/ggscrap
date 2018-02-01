# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class ZlqhSpider(GGFundNoticeSpider):
    name = 'FundNotice_Zlqh'
    sitename = '中粮期货'
    channel = '公告'
    entry = 'http://www.zlqh.com/index.php?optionid=8561'
    allowed_domains = ['www.ddqh.com']
    start_urls = []

    lps = [
        {
            'url': 'http://www.zlqh.com/index.php?optionid=8561',
            'ref': None
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(ZlqhSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        optionids = ['8561','8562','8563']
        for optionid in optionids:
            self.ips.append({
                'url': 'http://www.zlqh.com/index.php?optionid=' + optionid,
                'ref': response.url,
            })

        yield self.request_next()

    def parse_item(self, response):
        lis = response.xpath('//div[@class="ST18"]/ul/li')
        next_url = response.xpath('//div[@class="pagePanel"]/ul/li[last()]/a/@href').extract_first()
        for li in lis:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry

            span = li.xpath('./span')
            if len(span) != 0:
                url = li.xpath('./a/@href').extract_first()
                item['url'] = urljoin(get_base_url(response), url)

                item['title'] = li.xpath('./a/@title').extract_first()

                publish_time = li.xpath('./span/text()').extract_first()
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                yield item

        if next_url != '#':
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url,
            })

        yield self.request_next()


