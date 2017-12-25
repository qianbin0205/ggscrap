# -*- coding: utf-8 -*-

from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
from datetime import datetime
import re


class P5wNewsSpider(GGNewsSpider):
    name = 'News_P5w'
    sitename = '全景股票'
    allowed_domains = ['p5w.net']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(P5wNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '港股频道-港股新闻',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/stock/hkstock/hknews/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/stock/hkstock/hknews/index.htm'
            },
            {
                'ch': {
                    'name': '基金-要闻',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/fund/yw/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/fund/yw/'
            },
            {
                'ch': {
                    'name': '基金-分析评论',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/fund/fxpl/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/fund/fxpl/'
            },
            {
                'ch': {
                    'name': '基金-行业动态',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/fund/gsdt/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/fund/gsdt/'
            },
            {
                'ch': {
                    'name': '基金-私募基金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/fund/smjj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/fund/smjj/'
            },
            {
                'ch': {
                    'name': '基金-洞察基金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/fund/dcjh/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/fund/dcjh/'
            },
            {
                'ch': {
                    'name': '基金-创投基金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/fund/gqjj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/fund/gqjj/'
            },
            {
                'ch': {
                    'name': '理财-债券',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/money/zqzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/money/zqzx/'
            },
            {
                'ch': {
                    'name': '期货频道',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/futures/zhzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/futures/zhzx/'
            },
            {
                'ch': {
                    'name': '外汇频道',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/forex/news/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/forex/news/'
            },
            {
                'ch': {
                    'name': '财经-国内财经',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/news/gncj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/news/gncj/'
            },
            {
                'ch': {
                    'name': '财经-国际财经',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/news/gjcj/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/news/gjcj/'
            },
            {
                'ch': {
                    'name': '理财-银行资讯',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/money/yhzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/money/yhzx/'
            },
            {
                'ch': {
                    'name': '理财-保险资讯',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/money/bxzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/money/bxzx/'
            },
            {
                'ch': {
                    'name': '理财-信托资讯',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://www.p5w.net/money/xtzx/index'
                                  + (('_' + str(pg)) if pg >= 1 else '') + '.htm',
                'ref': 'http://www.p5w.net/money/xtzx/'
            }

        ]

        # url = 'http://www.p5w.net/kuaixun/201703/t20170330_1752522.htm'
        # url = 'http://www.p5w.net/stock/news/newstock/201402/t20140219_486436.htm'
        # url = 'http://www.p5w.net/kuaixun/201712/t20171220_2048325.htm'
        # url = 'http://www.p5w.net/kuaixun/201712/t20171220_2048306.htm'
        # url = 'http://www.p5w.net/stock/xingu/dingjia/201208/t20120801_25007.htm'
        # url = 'http://www.p5w.net/kuaixun/201712/t20171221_2049087.htm'
        # url = 'http://www.p5w.net/stock/news/zonghe/201712/t20171222_2049563.htm'
        # url = 'http://www.p5w.net/fund/dcjh/201601/t20160118_1330271.htm'
        # url = 'http://www.p5w.net/forex/news/201701/t20170105_1685546.htm'
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

        base = get_base_url(response)

        urls = response.xpath("//div[@class='manlist3']/ul/li//a/@href | //div[@class='left']//span[@class='hei']/a/@href").extract()
        for u in urls:
            u = urljoin(base, u)
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
        ls = response.css(".Custom_UnionStyle>*, .Custom_UnionStyle::text").extract()
        if len(ls) < 1:
            ls = response.css(
                ".article_content2>.TRS_Editor>*:not(p:nth-last-child(1)[align='center']), .article_content2>.TRS_Editor::text").extract()
        if len(ls) < 1:
            ls = response.css(".text>.TRS_Editor>*, .text>.TRS_Editor::text").extract()
        if len(ls) < 1:
            ls = response.css(".text>*, .kchart>.new_content_pic>*, .text::text").extract()
        if len(ls) < 1:
            ls = response.css(".article_content2>*:not(.headAd.contentAdv_3), .article_content2::text").extract()
        content = ''.join(ls)
        if 'item' in ext:
            item = ext['item']
            item['content'] = item['content'] + content
        else:
            item = GGNewsItem()
            item["content"] = content
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url'] = response.url
            title = response.xpath("//h1/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='title']/span/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='title']/text()").extract_first()
            item["title"] = title
            year = response.url.rsplit('/', 1)[1][1:5]
            pubtime = response.xpath("//span[@class='left']/time/text()").extract_first()
            if pubtime is not None:
                pubtime = year + "年" + pubtime
                pubtime = datetime.strptime(pubtime, '%Y年%m月%d日 %H:%M')
                pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
            item["pubtime"] = pubtime
            if item["pubtime"] is None:
                pubtime = response.xpath("//div[@class='source']/span").re_first(r"发布时间：(.*?)\s*作者")
                if pubtime is None:
                    pubtime = response.xpath("//div[@class='source']/text()").re_first(r"\d+年\d+月\d+日\s*\d+:\d+")
                if pubtime is None:
                    pubtime = response.xpath("//div[@class='title_3']/text()").re_first(r"\d+年\d+月\d+日\s*\d+:\d+")
                if pubtime is not None:
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日 %H:%M')
                    pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
                item["pubtime"] = pubtime
            item["source"] = response.xpath("//span[@class='left']/i[1]//text()").extract_first()
            if item["source"] is None:
                item["source"] = response.xpath("//div[@class='source']/span/ins/text()").extract_first()
            if item['source'] is None:
                item['source'] = response.xpath("//div[@class='source']/span/ins/a/text()").extract_first()
            if item['source'] is None:
                item['source'] = response.xpath("//div[@class='source']/a/text()").extract_first()
            if item['source'] is None:
                item['source'] = response.xpath("//div[@class='source']/span/a/text()").extract_first()
            if item['source'] is None:
                item['source'] = response.xpath("//div[@class='source']/span/text()").re_first(r'来源：(\S+)\s*发布时间：')
            if item['source'] is None:
                item['source'] = response.xpath("//div[@class='title_3']/ins/text()").extract_first()
            author = response.xpath("//span[@class='left']/i[3]/text()").extract_first()
            if author is None:
                author = response.xpath("//div[@class='source']/span").re_first(r"作者：(\S+)\s*")
            if author is None:
                author = response.xpath("//div[@class='title_3']/text()").re_first(r"作者：(\S+)\s*")
            item["author"] = author

        i = response.css('.viciao').re_first(r'createPageHTML\(\d+,(\d+),"\w+","htm"\);')  # 当前页号
        c = response.css('.viciao').re_first(r'createPageHTML\((\d+),\d+,"\w+","htm"\);')  # 总计页数
        if i is None or c is None:
            yield item
            ch['count'] = ch['count'] + 1
        elif int(i) >= int(c) - 1:
            yield item
            ch['count'] = ch['count'] + 1
        else:
            rcs.insert(0, {
                'ch': ch,
                'url': re.sub(r'(t[0-9]+?_[0-9]+?)(_[0-9]+?|)(?=\.htm)', r'\1_' + str(int(i) + 1), response.url,
                              flags=re.I),
                'ref': response.url,
                'ext': {'item': item}
                })
        yield self.request_next(cps, rcs, nps)
