# -*- coding: utf-8 -*-

from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
from datetime import datetime
import re


class Jj21NewsSpider(GGNewsSpider):
    name = 'News_Jj21'
    sitename = '21经济网'
    allowed_domains = ['21jingji.com']
    start_urls = [
        'http://www.21jingji.com/channel/herald/',
        'http://www.21jingji.com/channel/business/'
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(Jj21NewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '商业',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://www.21jingji.com/channel/business/' + ((str(pg) + '.html') if pg >= 2 else ''),
                'ref': 'http://www.21jingji.com/channel/business/'
            },
            {
                'ch': {
                    'name': '抢鲜报',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://www.21jingji.com/channel/herald/' + ((str(pg) + '.html') if pg >= 2 else ''),
                'ref': 'http://www.21jingji.com/channel/herald/'
            }
        ]
        # url = 'http://www.21jingji.com/2017/12-7/5NMDEzNzlfMTQyMTQ5NQ.html'
        # url = 'http://www.21jingji.com/2017/12-7/5NMDEzNzlfMTQyMTQ5NA.html'
        # url = 'http://www.21jingji.com/2017/12-7/5MMDEzNzlfMTQyMTQ5Mg.html'
        # url = 'http://www.21jingji.com/2017/12-20/zMMDEzNzlfMTQyMjIzMw.html'
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

        urls = response.xpath("//div[@id='data_list']/div/div[@class='Tlist']/a/@href").extract()
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
        ls = response.xpath("//div[@class='detailCont']/p").extract()
        if len(ls) < 1:
            ls = response.xpath("//div[@class='txtContent']/p").extract()
        content = ''.join(ls)
        if content is not None:
            content = content.replace('返回21经济首页&gt;&gt;', '')
        if 'item' in ext:
            item = ext['item']
            item['content'] = item['content'] + content
        else:
            item = GGNewsItem()
            item["content"] = content
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['entry'] = ch['entry']
            item['url'] = response.url
            title = response.xpath("//h2/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='titleHead']/h1/text()").extract_first()
            item['title'] = title

            source = response.xpath("//span[@class='baodao']/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='newsInfo']/text()").re_first(r'\S+')
            item['source'] = source

            item['author'] = response.xpath("//span[@class='Wh1']/text()").extract_first()

            pubtime = response.xpath("//div[@class='newsDate']/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//p[@class='Wh']/span[1]/text()").extract_first() + response.xpath(
                "//p[@class='Wh']/span[2]/text()").extract_first()
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = re.sub(r'\s+', '', pubtime.strip())
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日%H:%M')
                    pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
            item['pubtime'] = pubtime

        currentPageurl = response.url
        nextPageurl = response.xpath("//a[text()='下一页']/@href").extract_first()
        if nextPageurl is None or currentPageurl == nextPageurl:
            yield item
            ch['count'] = ch['count'] + 1
        else:
            rcs.insert(0, {
                'ch': ch,
                'url': nextPageurl,
                'ref': response.url,
                'ext': {'item': item}
            })

        yield self.request_next(cps, rcs, nps)
