# -*- coding: utf-8 -*-

import re
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider


class ZzwCsNewsSpider(GGNewsSpider):
    name = 'ZzwCsNews'
    sitename = '中证网'
    allowed_domains = ['www.cs.com.cn']
    start_urls = ['http://www.cs.com.cn/ssgs/hyzx/']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, limit=None, *args, **kwargs):
        super(ZzwCsNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '公司-行业',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/ssgs/hyzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/ssgs/hyzx/'
            }
        ]

        # url = 'http://www.cs.com.cn/ssgs/hyzx/201710/t20171023_5527572.html'
        # url = 'http://www.cs.com.cn/ssgs/hyzx/201711/t20171120_5579232.html'
        # url = 'http://www.cs.com.cn/ssgs/hyzx/201711/t20171120_5578996.html'
        # cp = cps[0]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_link(self, response):
        ch = response.meta['ch']
        pg = response.meta['pg']
        url = response.meta['url']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']

        urls = response.css('body>.box1000>.box740.fl>dl>dt>a::attr(href)').extract()
        for u in urls:
            u = urljoin(get_base_url(response), u)
            rcs.append({
                'ch': ch,
                'url': u,
                'ref': response.url
            })

        nps.append({
            'ch': ch,
            'pg': pg + 1,
            'url': url,
            'ref': response.url
        })

        yield self.request_next(cps, rcs, nps)

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
