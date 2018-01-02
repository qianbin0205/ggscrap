# -*- coding: utf-8 -*-

import html
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider


class NbdNewsSpider(GGNewsSpider):
    name = 'News_Nbd'
    sitename = '每经网'
    allowed_domains = ['nbd.com.cn']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(NbdNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            # {
            #     'ch': {
            #         'name': '要闻',
            #         'count': 0
            #     },
            #     'url': 'http://www.nbd.com.cn/columns/3',
            #     'ref': 'http://www.nbd.com.cn/columns/3'
            # },
            # {
            #     'ch': {
            #         'name': '证券-重磅推荐',
            #         'count': 0
            #     },
            #     'url': 'http://stocks.nbd.com.cn/columns/318',
            #     'ref': 'http://stocks.nbd.com.cn/columns/318'
            # },
            # {
            #     'ch': {
            #         'name': '证券-两融龙虎榜',
            #         'count': 0
            #     },
            #     'url': 'http://stocks.nbd.com.cn/columns/402',
            #     'ref': 'http://stocks.nbd.com.cn/columns/402'
            # },
            # {
            #     'ch': {
            #         'name': '证券-A股动态',
            #         'count': 0
            #     },
            #     'url': 'http://stocks.nbd.com.cn/columns/275',
            #     'ref': 'http://stocks.nbd.com.cn/columns/275'
            # },
            # {
            #     'ch': {
            #         'name': '证券-公告速递',
            #         'count': 0
            #     },
            #     'url': 'http://stocks.nbd.com.cn/columns/28',
            #     'ref': 'http://stocks.nbd.com.cn/columns/28'
            # },
            # {
            #     'ch': {
            #         'name': '公司-热点公司',
            #         'count': 0
            #     },
            #     'url': 'http://industry.nbd.com.cn/columns/346',
            #     'ref': 'http://industry.nbd.com.cn/columns/346'
            # },
            # {
            #     'ch': {
            #         'name': '公司-重磅调查',
            #         'count': 0
            #     },
            #     'url': 'http://industry.nbd.com.cn/columns/587',
            #     'ref': 'http://industry.nbd.com.cn/columns/587'
            # },
            # {
            #     'ch': {
            #         'name': '证券-海外市场',
            #         'count': 0
            #     },
            #     'url': 'http://stocks.nbd.com.cn/columns/405',
            #     'ref': 'http://stocks.nbd.com.cn/columns/405'
            # },
            # {
            #     'ch': {
            #         'name': '理财-重磅原创',
            #         'count': 0
            #     },
            #     'url': 'http://money.nbd.com.cn/columns/440',
            #     'ref': 'http://money.nbd.com.cn/columns/440'
            # },
            # {
            #     'ch': {
            #         'name': '理财-基金投资',
            #         'count': 0
            #     },
            #     'url': 'http://money.nbd.com.cn/columns/441',
            #     'ref': 'http://money.nbd.com.cn/columns/441'
            # },
            # {
            #     'ch': {
            #         'name': '公司-产业趋势',
            #         'count': 0
            #     },
            #     'url': 'http://industry.nbd.com.cn/columns/585',
            #     'ref': 'http://industry.nbd.com.cn/columns/585'
            # },
            # {
            #     'ch': {
            #         'name': '公司-商业人物',
            #         'count': 0
            #     },
            #     'url': 'http://industry.nbd.com.cn/columns/418',
            #     'ref': 'http://industry.nbd.com.cn/columns/418'
            # },
            # {
            #     'ch': {
            #         'name': '公司-区域经济',
            #         'count': 0
            #     },
            #     'url': 'http://industry.nbd.com.cn/columns/586',
            #     'ref': 'http://industry.nbd.com.cn/columns/586'
            # },
            {
                'ch': {
                    'name': '国际-头条',
                    'count': 0
                },
                'url': 'http://world.nbd.com.cn/columns/597',
                'ref': 'http://world.nbd.com.cn/columns/597'
            },
            {
                'ch': {
                    'name': '国际-华尔街前哨',
                    'count': 0
                },
                'url': 'http://world.nbd.com.cn/columns/598',
                'ref': 'http://world.nbd.com.cn/columns/598'
            },
            {
                'ch': {
                    'name': '国际-科技情报站',
                    'count': 0
                },
                'url': 'http://world.nbd.com.cn/columns/599',
                'ref': 'http://world.nbd.com.cn/columns/599'
            },
            {
                'ch': {
                    'name': '国际-天下热闻',
                    'count': 0
                },
                'url': 'http://world.nbd.com.cn/columns/600',
                'ref': 'http://world.nbd.com.cn/columns/600'
            },
            {
                'ch': {
                    'name': '国际-全球财经早报',
                    'count': 0
                },
                'url': 'http://world.nbd.com.cn/columns/603',
                'ref': 'http://world.nbd.com.cn/columns/603'
            },
            {
                'ch': {
                    'name': '金融-要闻',
                    'count': 0
                },
                'url': 'http://finance.nbd.com.cn/columns/329',
                'ref': 'http://finance.nbd.com.cn/columns/329'
            },
            {
                'ch': {
                    'name': '金融-监管',
                    'count': 0
                },
                'url': 'http://finance.nbd.com.cn/columns/415',
                'ref': 'http://finance.nbd.com.cn/columns/415'
            },
            {
                'ch': {
                    'name': '金融-机构',
                    'count': 0
                },
                'url': 'http://finance.nbd.com.cn/columns/327',
                'ref': 'http://finance.nbd.com.cn/columns/327'
            },
            {
                'ch': {
                    'name': '金融-市场',
                    'count': 0
                },
                'url': 'http://finance.nbd.com.cn/columns/326',
                'ref': 'http://finance.nbd.com.cn/columns/326'
            },
            {
                'ch': {
                    'name': '金融-新金融周刊',
                    'count': 0
                },
                'url': 'http://finance.nbd.com.cn/columns/591',
                'ref': 'http://finance.nbd.com.cn/columns/591'
            },
            {
                'ch': {
                    'name': '金融-保险周刊',
                    'count': 0
                },
                'url': 'http://finance.nbd.com.cn/columns/592',
                'ref': 'http://finance.nbd.com.cn/columns/592'
            },
            {
                'ch': {
                    'name': '宏观-要闻',
                    'count': 0
                },
                'url': 'http://economy.nbd.com.cn/columns/44',
                'ref': 'http://economy.nbd.com.cn/columns/44'
            },
            {
                'ch': {
                    'name': '宏观-焦点',
                    'count': 0
                },
                'url': 'http://economy.nbd.com.cn/columns/313',
                'ref': 'http://economy.nbd.com.cn/columns/313'
            },
            {
                'ch': {
                    'name': '宏观-形势',
                    'count': 0
                },
                'url': 'http://economy.nbd.com.cn/columns/315',
                'ref': 'http://economy.nbd.com.cn/columns/315'
            },
            {
                'ch': {
                    'name': '宏观-洞见',
                    'count': 0
                },
                'url': 'http://economy.nbd.com.cn/columns/475',
                'ref': 'http://economy.nbd.com.cn/columns/475'
            },
        ]
        # url = 'http://www.nbd.com.cn/articles/2018-01-01/1178115.html'
        # url = 'http://m.nbd.com.cn/articles/2018-01-01/1178051.html'
        # url = 'http://www.nbd.com.cn/articles/2015-08-24/940840.html'
        # cp = cps[0]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_link(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']

        base = get_base_url(response)

        urls = response.xpath("//div[@class='m-list']/ul/li/a/@href").extract()
        for url in urls:
            url = urljoin(base, url)
            rcs.append({
                'ch': ch,
                'url': url,
                'ref': response.url
            })

        url = response.xpath("//span[@class='next']/a/@href").extract_first()
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

        ls = response.css('.g-articl-text>*:not(center):not(.paginationWrapper), .g-article-abstract>p, .g-articl-text::text').extract()
        if len(ls) < 1:
            ls = response.css("#vedioPlayer>*").extract()
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
            title = response.xpath("//div[@class='g-article-top']/h1/text()").re_first(r'\S+')
            if title is None:
                title = response.xpath("//div[@class='nbd-con']/h1/text()").extract_first()
            item["title"] = title

            pubtime = response.xpath("//span[@class='time']/text()").re_first(r"(\d+-\d+-\d+\s*\d+:\d+:\d+)")
            year = response.url.rsplit('/', 2)[1][0:4]
            if pubtime is None:
                pubtime = response.xpath("//p[@class='article-meta']/small/text()").re_first("\d+-\d+\s*\d+:\d+")
                if pubtime is not None:
                    pubtime = year + '-' + pubtime
            item["pubtime"] = pubtime

            source = response.xpath("//span[@class='source']/text()").re_first(r'\s*(\S+)\s*|')
            if source is None:
                source = response.xpath("//span[@class='source']/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='article-meta']/small/text()").re_first(r'\s*(\S+)\s*\d+-\d+\s*\d+:\d+')
            item['source'] = source

            item["author"] = response.xpath("//span[@class='source']/text()").re_first(r'|\s*(\S+)\s*')

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
