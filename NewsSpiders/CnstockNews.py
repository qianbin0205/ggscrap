# -*- coding: utf-8 -*-

import re
from urllib import parse
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
import json


class CnstockNewsSpider(GGNewsSpider):
    name = 'News_Cnstock'
    sitename = '中国证券网'
    allowed_domains = ['cnstock.com']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(CnstockNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '上证快讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://app.cnstock.com/api/xcx/kx?callback=&colunm=szkx&num=15&page=' + str(pg),
                'ref': 'http://news.cnstock.com/bwsd/index.html'
            },
            {
                'ch': {
                    'name': '产业-期货-上证4小时',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://app.cnstock.com/api/theme/get_theme_list?callback=&size=10&maxid=0&minid='
                                  + (str(201-pg*10)if pg >= 1 else '0'),
                'ref': 'http://news.cnstock.com/theme/index.html'
            },
            {
                'ch': {
                    'name': '产业-期货-产业淘金',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://app.cnstock.com/api/taojin/get_theme_list?callback=&size=10&maxid=0&minid='
                                  + (str(51-pg*10)if pg >= 1 else '0'),
                'ref': 'http://news.cnstock.com/industry/taojin/index.html'
            },
        ]

        # cp = cps[0]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_link(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']
        url = response.meta['url']
        pg = response.meta['pg']

        base = get_base_url(response)
        if ch['name'] == '产业-期货-产业淘金':
            data = json.loads(response.text)['item']
            urls = [i['docurl'] for i in data]
        elif ch['name'] == '产业-期货-上证4小时':
            data = json.loads(response.text)['item']
            urls = [('http://news.cnstock.com/theme,' + i['id'] +'.html') for i in data]
        else:
            data = json.loads(response.text)['item']
            urls = [i['link'] for i in data]
        for u in urls:
            u = urljoin(base, u)
            rcs.append({
                'ch': ch,
                'url': u,
                'ref': response.url
            })

        nps.append({
            'ch': ch,
            'pg': pg+1,
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

        if not response.css('#pager-content'):
            if re.match(r'^http://news[.]cnstock[.]com/theme,[0-9]+[.]html$', response.url) is not None:
                url = response.css('.tcbhd-r>h1>a::attr(href)').extract_first()
                url = urljoin(get_base_url(response), url)
                rcs.append({
                    'ch': ch,
                    'url': url,
                    'ref': response.url
                })
        else:
            ls = response.css('#qmt_content_div>.doc_4162799_0>p').extract()
            if len(ls) < 1:
                ls = response.css("#qmt_content_div>*:not(#contentPager):not(input):not(#output_hangqing_div)").extract()
            if len(ls) < 1:
                ls = response.xpath("//div[@class='content-inner']/p").extract()
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
                title = response.css('.main-content>h1.title::text').extract_first()
                if title is None:
                    title = response.xpath("//div[@class='title-inner']/h1/text()").extract_first()
                item['title'] = title
                if 'PK台' in item['title']:
                    yield self.request_next(cps, rcs, nps)
                    return

                source = response.css('.main-content>.bullet>span.source>a::text').extract_first()
                if source is None:
                    source = response.css('.main-content>.bullet>span.source::text').extract_first()
                if source is None:
                    source = response.xpath("//div[@class='sub-title']/strong/a/text()").extract_first()
                if source is not None:
                    source = source.replace('来源：', '')
                item['source'] = source

                author = response.css('.main-content>.bullet>span.author::text').extract_first()
                if author is not None:
                    author = author.replace('作者：', '')
                item['author'] = author

                pubtime = response.css('.main-content>.bullet>span.timer::text').extract_first()
                if pubtime is None:
                    pubtime = response.xpath("//div[@class='sub-title']/span[@class='time']/text()").extract_first()
                item['pubtime'] = pubtime

            q = parse.parse_qs(parse.urlparse(response.url).query)
            pg = int(q['page'][0]) if 'page' in q else 1
            c = int(response.css('#hid_totalPage::attr(value)').extract_first())
            if pg < c:
                rcs.insert(0, {
                    'ch': ch,
                    'url': item['url'] + '?page=' + str(pg + 1),
                    'ref': response.url,
                    'ext': {'item': item}
                })
            else:
                yield item
                ch['count'] = ch['count'] + 1

        yield self.request_next(cps, rcs, nps)
