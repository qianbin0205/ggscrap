# -*- coding: utf-8 -*-

import re
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider


class ZzwCsNewsSpider(GGNewsSpider):
    name = 'News_ZzwCs'
    sitename = '中证网'
    allowed_domains = ['cs.com.cn']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(ZzwCsNewsSpider, self).__init__(limit, *args, **kwargs)

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
            },
            {
                'ch': {
                    'name': '基金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/tzjj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/tzjj/'
            },
            {
                'ch': {
                    'name': '基金-公募基金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/tzjj/jjdt/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/tzjj/jjdt/'
            },
            {
                'ch': {
                    'name': '基金-基金视点',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/tzjj/jjks/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/tzjj/jjks/'
            },
            {
                'ch': {
                    'name': '基金-基金持仓',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/tzjj/jjcs/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/tzjj/jjcs/'
            },
            {
                'ch': {
                    'name': '基金-私募基金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/tzjj/smjj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/tzjj/smjj/'
            },
            {
                'ch': {
                    'name': '基金-投基天地',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/tzjj/tjdh/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/tzjj/tjdh/'
            },
            {
                'ch': {
                    'name': '期市',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/zzqh/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/zzqh/'
            },
            {
                'ch': {
                    'name': '期市-商品期货',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/zzqh/spqh/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/zzqh/spqh/'
            },
            {
                'ch': {
                    'name': '期市-金融衍生品',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/zzqh/ysp/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/zzqh/ysp/'
            },
            {
                'ch': {
                    'name': '市场-行业研究',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/gppd/hyyj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/gppd/hyyj/'
            },
            {
                'ch': {
                    'name': '新闻-海外消息',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/xwzx/hwxx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/xwzx/hwxx/'
            },
            {
                'ch': {
                    'name': '新闻',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/xwzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/xwzx/'
            },
            {
                'ch': {
                    'name': '新闻-民生视角',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.cs.com.cn/xwzx/ms/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.shtml',
                'ref': 'http://www.cs.com.cn/xwzx/ms/'
            },
        ]
        # url = 'http://www.cs.com.cn/gg/hgt/201512/t20151211_4860111.html'
        # cp = cps[2]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_list(self, response):
        ch = response.meta['ch']
        pg = response.meta['pg']
        url = response.meta['url']
        cps = response.meta['cps']
        ips = response.meta['ips']
        nps = response.meta['nps']

        dls = response.css('body>.box1000>.box740.fl>dl')
        for dl in dls:
            u = dl.xpath("./dt/a/@href").extract_first()
            u = urljoin(get_base_url(response), u)
            pubtime = dl.xpath("./dd/span/text()").extract_first()
            ips.append({
                'ch': ch,
                'url': u,
                'ext': {'pubtime':pubtime},
                'ref': response.url
            })

        nps.append({
            'ch': ch,
            'pg': pg + 1,
            'url': url,
            'ref': response.url
        })

        yield self.request_next(cps, ips, nps)

    def parse_item(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        ips = response.meta['ips']
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
            item['entry'] = ch['entry']
            item['url'] = response.url

            title = response.xpath(
                "//div[@class='artical_t']/h1/text()|//div[@class='column-box']/h1/text()").extract_first()
            if title is None:
                title = response.css("#img-content>h2::text").re_first(r'\S+')
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

            if ext['pubtime'] is not None:
                item['pubtime'] = '20' + ext['pubtime']
            # pubtime = response.xpath("//div[@class='artical_t']/span/text()").re_first(r'\d+-\d+-\d+\s*\d+:\d+')
            # if pubtime is None:
            #     pubtime = response.xpath("//div[@class='column-sub']/span/text()").re_first(r'\d+-\d+-\d+\s*\d+:\d+')
            # if pubtime is None:
            #     pubtime = response.css("#meta_content>#post-date::text").extract_first()
            # if pubtime is not None:
            #     if len(pubtime) == 16:
            #         pubtime = pubtime + ':00'
            #     item['pubtime'] = pubtime

        i = response.css('.artical_c .page, .z_list_page').re_first(r'var\s+?currentPage\s+?=\s+?(\d+)')  # 当前页号
        c = response.css('.artical_c .page, .z_list_page').re_first(r'var\s+?countPage\s+?=\s+?(\d+)')  # 总计页数
        if i is None or c is None:
            yield item
            ch['count'] = ch['count'] + 1
        elif int(i) >= int(c) - 1:
            yield item
            ch['count'] = ch['count'] + 1
        else:
            ips.insert(0, {
                'ch': ch,
                'url': re.sub(r'(t[0-9]+?_[0-9]+?)(_[0-9]+?|)(?=\.html)', r'\1_' + str(int(i) + 1), response.url,
                              flags=re.I),
                'ref': response.url,
                'ext': {'item': item}
            })

        yield self.request_next(cps, ips, nps)
