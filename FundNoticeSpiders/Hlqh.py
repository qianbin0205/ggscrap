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
    allowed_domains = ['www.hlqh.com']
    start_urls = ['http://www.hlqh.com']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'UM_distinctid=160e95cb88f89-04accda377420c-393d5c04-15f900-160e95cb8903cc; _cnzz_CV4130363=toJSONString%7C%7C; real_ipd=203.110.179.245; ECS_ID=3d5ec8feca7c554aa88f9d32efb51b96169b5c97; CNZZDATA4130363=cnzz_eid%3D685787141-1515741960-http%253A%252F%252Fwww.hlqh.com%252F%26ntime%3D1517311255; td_cookie=11049176; ECS[display]=grid; noHint=1'

    lps = [
        {
            'ch': {
                'name': '产品公告',
                'url_entry': 'http://www.hlqh.com/article_cat.php?id=62',
                'count': 0
            },
            'url': 'http://www.hlqh.com/article_cat.php?id=62',
            'ref': 'http://www.hlqh.com/index.php'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(HlqhSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):

        yield self.request_next()

    def parse_list(self, response):
        pi = response.meta['pi']
        ch = pi['ch']

        funds = response.xpath("//ul[@class='news-list']/li")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url_entry'] = ch['url_entry']
            url = fund.xpath("./a/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = fund.xpath("./a/em/text()").extract_first()
            publish_time = fund.xpath("./span/text()").extract_first()
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            self.lps.append({
                'ch': ch,
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })

        yield self.request_next()


