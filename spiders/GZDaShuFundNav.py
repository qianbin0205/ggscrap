# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGFundNavSpider


class GZDaShuFundNavSpider(GGFundNavSpider):
    name = 'GZDaShuFundNav'
    sitename = '广州大树投资'
    allowed_domains = ['www.gzdashu.com']
    start_urls = ['http://www.gzdashu.com/cpzx.aspx']

    def __init__(self, limit=None, *args, **kwargs):
        super(GZDaShuFundNavSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.gzdashu.com/cpzx.aspx',
                'ref': 'http://www.gzdashu.com/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        funds = response.xpath('//a[starts-with(@id,"qxcp")]').extract()
        print(funds)

    def parse_item(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']
        ext = response.meta['ext']

        content = None
        ls = response.css('.artical_c>.blank10').xpath('./preceding-sibling::div/div/*').extract()
        if len(ls) >= 1:
            content = ''.join(ls)
        if content is None:
            ls = response.css('.artical_c>.blank10').xpath('./preceding-sibling::div/*').extract()
            if len(ls) >= 1:
                content = ''.join(ls)
        if content is None:
            ls = response.css('.artical_c>.blank10').xpath('./preceding-sibling::*').extract()
            if len(ls) >= 1:
                content = ''.join(ls)
        if content is None:
            content = ''

        if 'item' in ext:
            item = ext['item']
            item['content'] = item['content'] + content
        else:
            item = GGNewsItem()
            item['content'] = content

            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url'] = response.url

            item['title'] = response.css('.artical_t>h1::text').extract_first()
            item['source'] = response.css('.artical_t>span:nth-of-type(2)::text').extract_first()
            item['author'] = response.css('.artical_t>span:nth-of-type(1)::text').extract_first()

            pubtime = response.css('.artical_t>span.Ff::text').extract_first()
            if pubtime is not None:
                if len(pubtime) == 16:
                    pubtime = pubtime + ':00'
                item['pubtime'] = pubtime

        i = int(response.css('.artical_c>.page').re_first(r'var\s+?currentPage\s+?=\s+?(\d+)'))  # 当前页号
        c = int(response.css('.artical_c>.page').re_first(r'var\s+?countPage\s+?=\s+?(\d+)'))  # 总计页数
        if i < c - 1:
            rcs.insert(0, {
                'ch': ch,
                'url': re.sub(r'(t[0-9]+?_[0-9]+?)(_[0-9]+?|)(?=\.html)', r'\1_' + str(i + 1), response.url,
                              flags=re.I),
                'ref': response.url,
                'ext': {'item': item}
            })
        else:
            yield item
            ch['count'] = ch['count'] + 1

        yield self.request_next(cps, rcs, nps)
