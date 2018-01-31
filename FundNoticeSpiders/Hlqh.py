# -*- coding: utf-8 -*-

import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class HlqhSpider(GGFundNoticeSpider):
    name = 'FundNotice_Hlqh'
    sitename = '华联期货'
    channel = '公告'
    entry = 'http://www.hlqh.com/article_cat.php?id=62'
    allowed_domains = ['www.hlqh.com']
    start_urls = ['http://www.hlqh.com']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'UM_distinctid=160e95cb88f89-04accda377420c-393d5c04-15f900-160e95cb8903cc; _cnzz_CV4130363=toJSONString%7C%7C; ECS[display]=grid; noHint=1; real_ipd=203.110.179.245; ECS_ID=22a1cde20caabfa5307ebaabbd44ac90c69b18d8; CNZZDATA4130363=cnzz_eid%3D685787141-1515741960-http%253A%252F%252Fwww.hlqh.com%252F%26ntime%3D1517362036; td_cookie=11049100'

    lps = [
        {
            'url': 'http://www.hlqh.com/article_cat.php?id=62',
            'ref': 'http://www.hlqh.com/index.php'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(HlqhSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        funds = response.xpath("//ul[@class='news-list']/li")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            url = fund.xpath("./a/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = fund.xpath("./a/em/text()").extract_first()
            publish_time = fund.xpath("./span/text()").extract_first()
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            self.lps.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })

        yield self.request_next()


