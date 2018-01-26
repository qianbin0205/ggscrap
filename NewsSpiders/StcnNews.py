# -*- coding: utf-8 -*-

import html
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider


class StcnNewsSpider(GGNewsSpider):
    name = 'News_Stcn'
    sitename = '证券时报网'
    allowed_domains = ['stcn.com']
    start_urls = []

    handle_httpstatus_list = [404]

    def __init__(self, limit=None, *args, **kwargs):
        super(StcnNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {

                'ch': {
                    'name': '机构-期货',
                    'count': 0
                },
                'url': 'http://finance.stcn.com/qihuo/index.shtml',
                'ref': 'http://finance.stcn.com/qihuo/index.shtml'
            },
            {

                'ch': {
                    'name': '机构-券商',
                    'count': 0
                },
                'url': 'http://finance.stcn.com/quanshang/index.shtml',
                'ref': 'http://finance.stcn.com/quanshang/index.shtml'
            },
            {
                'ch': {
                    'name': '机构-银行理财',
                    'count': 0
                },
                'url': 'http://finance.stcn.com/yxlc/index.shtml',
                'ref': 'http://finance.stcn.com/yxlc/index.shtml'
            },
            {
                'ch': {
                    'name': '机构-保险',
                    'count': 0
                },
                'url': 'http://finance.stcn.com/baoxian/index.shtml',
                'ref': 'http://finance.stcn.com/baoxian/index.shtml'
            },
            {
                'ch': {
                    'name': '机构-信托',
                    'count': 0
                },
                'url': 'http://finance.stcn.com/xintuo/index.shtml',
                'ref': 'http://finance.stcn.com/xintuo/index.shtml'
            },
        ]

        # url = 'http://data.stcn.com/2017/1213/13831061.shtml'
        # cp = cps[3]

        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_link(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']

        base = get_base_url(response)

        urls = response.xpath(
            "//div[@id='mainlist']/ul/li/p/a[not(@class)]/@href | //div[@class='maj_box_list']/ul/li/a/@href").extract()
        for url in urls:
            url = urljoin(base, url)
            rcs.append({
                'ch': ch,
                'url': url,
                'ref': response.url
            })

        url = response.xpath("//a[text()='下一页']/@href|//a[text()='>']/@href").extract_first()
        if url is not None:
            url = html.unescape(url)
            url = urljoin(base, url)
            nps.append({
                'ch': ch,
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
        ls = response.css('#ctrlfscont>*:not(.adv):not(.txt_zhu):not(.om), #ctrlfscont::text').extract()
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
            title = response.xpath("//div[@class='intal_tit']/h2/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='content_tit']/h2/text()").extract_first()
            item["title"] = title
            pubtime = response.xpath("//div[@class='content_tit']//span/text()").re_first(r"(\d+-\d+-\d+\s*\d+:\d+)")
            if pubtime is None:
                pubtime = response.xpath("//div[@class='info']/text()").re_first(r"(\d+-\d+-\d+\s*\d+:\d+)")
            item["pubtime"] = pubtime

            source = response.xpath("//div[@class='info']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='info']//text()").re_first(r"来源：\s*(\S+)\s*")
            if source is None:
                source = response.xpath("//div[@class='content_tit']/p/text()").re_first(r"来源：\s*(\S.*\S)\s*作者")
            if source is None:
                source = response.xpath("//div[@class='content_tit']/p/text()").re_first(r"来源：\s*(\S.*\S)\s*")
            item['source'] = source
            item["author"] = response.xpath("//div[@class='content_tit']/p/text()").re_first(r"作者：(.*?)\s+")

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is None:
            yield item
            ch['count'] = ch['count'] + 1
        else:
            rcs.insert(0, {
                'ch': ch,
                'url': next_url,
                'ref': response.url,
                'ext': {'item': item}
            })

        yield self.request_next(cps, rcs, nps)
