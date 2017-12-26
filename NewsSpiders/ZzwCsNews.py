# -*- coding: utf-8 -*-

import re
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider


class ZzwCsSpider(GGNewsSpider):
    name = 'News_ZzwCs'
    sitename = '中证网'
    allowed_domains = ['www.cs.com.cn']
    start_urls = ['http://www.cs.com.cn/ssgs/hyzx/']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, limit=None, *args, **kwargs):
        super(ZzwCsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '中证网栏目-中证十条',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/sylm/cstop10/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/sylm/cstop10/'
            },
            {
                'ch': {
                    'name': '中证网栏目-即时播报',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/sylm/jsxw/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/sylm/jsxw/'
            },
            {
                'ch': {
                    'name': '中证网栏目-观点评论',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/sylm/zjyl_1/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/sylm/zjyl_1/'
            },
            {
                'ch': {
                    'name': '港股',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/gg/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/gg/'
            },
            {
                'ch': {
                    'name': '港股-港股公司',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/gg/gsxw/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/gg/gsxw/'
            },
            {
                'ch': {
                    'name': '港股-投资评级',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/gg/tzpj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/gg/tzpj/'
            },
            {
                'ch': {
                    'name': '港股-沪港通',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/gg/hgt/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/gg/hgt/'
            },
            {
                'ch': {
                    'name': '港股-深港通',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/gg/sgt/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/gg/sgt/'
            },
            {
                'ch': {
                    'name': '港股-深港通',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/zqxw/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/zqxw/'
            },
            {
                'ch': {
                    'name': '债市-债市评论',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/zqxw/zspl/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/zqxw/zspl/'
            }
        ]
        # url = 'http://www.cs.com.cn/gg/hgt/201512/t20151211_4860111.html'
        # cp = cps[0]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        # yield self.request_next(cps, [], [])

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

        ls = response.css(".artical_c>.Custom_UnionStyle>*").extract()
        if len(ls) < 1:
            ls = response.css(".artical_c>.article_content2>*:not(.headAd.contentAdv_3)").extract()
        if len(ls) < 1:
            ls = response.css(
                ".artical_c>*:not(.page):not(.list_fj):not(.blank10):not(strong), .artical_c::text").extract()
        if len(ls) < 1:
            ls = response.css(".Dtext>*").extract()
        if len(ls) < 1:
            ls = response.css("#js_content>*").extract()
        content = ''.join(ls)

        if 'item' in ext:
            item = ext['item']
            item['content'] = item['content'] + content
        else:
            item = GGNewsItem()
            item['content'] = content

            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url'] = response.url

            title = response.xpath(
                "//div[@class='artical_t']/h1/text()|//div[@class='column-box']/h1/text()").extract_first()
            if title is None:
                title = response.css("#img-content>h2::text").extract_first()
            item['title'] = title

            source = response.xpath(
                "//div[@class='artical_t']/span[2]/text()|//div[@class='column-sub']/em[2]/text()").extract_first()
            if source is None:
                source = response.xpath("//a[@id='post-user']/text()").extract_first()
            item['source'] = source

            author = response.xpath(
                "//div[@class='artical_t']/span[1]/text()|//div[@id='meta_content']/em[2]/text()").extract_first()
            if author is None:
                author = response.xpath("//div[@class='column-sub']/em[1]/text()").re_first(r'作者：(\S+)')
            item['author'] = author

            pubtime = response.xpath("//div[@class='artical_t']/span/text()").re_first(r'\d+-\d+-\d+\s*\d+:\d+')
            if pubtime is None:
                pubtime = response.xpath("//div[@class='column-sub']/span/text()").re_first(r'\d+-\d+-\d+\s*\d+:\d+')
            if pubtime is None:
                pubtime = response.css("#meta_content>#post-date::text").extract_first()
            if pubtime is not None:
                if len(pubtime) == 16:
                    pubtime = pubtime + ':00'
                item['pubtime'] = pubtime

        i = response.css('.artical_c .page, .z_list_page').re_first(r'var\s+?currentPage\s+?=\s+?(\d+)')  # 当前页号
        c = response.css('.artical_c .page, .z_list_page').re_first(r'var\s+?countPage\s+?=\s+?(\d+)')  # 总计页数
        if i is None or c is None:
            yield item
            ch['count'] = ch['count'] + 1
        elif int(i) >= int(c) - 1:
            yield item
            ch['count'] = ch['count'] + 1
        else:
            rcs.insert(0, {
                'ch': ch,
                'url': re.sub(r'(t[0-9]+?_[0-9]+?)(_[0-9]+?|)(?=\.html)', r'\1_' + str(int(i) + 1), response.url,
                              flags=re.I),
                'ref': response.url,
                'ext': {'item': item}
            })

        yield self.request_next(cps, rcs, nps)
