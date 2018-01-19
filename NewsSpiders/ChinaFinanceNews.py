# -*- coding: utf-8 -*-

import html
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
from datetime import datetime


class ChinaFinanceNewsSpider(GGNewsSpider):
    name = 'News_ChinaFinance'
    sitename = '中国网财经'
    allowed_domains = ['china.com.cn']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(ChinaFinanceNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '证券-证券要闻',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/stock/zqyw/index.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '证券-市场风云',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/stock/dp/index.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '港股',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/stock/hkstock/index.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '美股',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/stock/usstock/index.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '基金',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/money/fund/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '理财-原创新闻',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/money/my.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '产经-原创新闻',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/industry/my.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '产经',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/industry/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '科技首页-科技滚动新闻',
                    'count': 0
                },
                'url': 'http://tech.china.com.cn/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '消费',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/consume/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '医药',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/industry/medicine/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '能源',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/industry/energy/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '产经-房产',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/industry/estate/index.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '新闻-滚动新闻',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/news/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-原创新闻',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/my.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '最新',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://news.china.com.cn/world/node_7208703' + (('_' + str(pg))if pg >= 2 else '') + '.htm',
                'ref': None
            },
            {
                'ch': {
                    'name': '国内要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://www.china.com.cn/news/local/node_7065265' + (('_' + str(pg))if pg >= 2 else '') + '.htm',
                'ref': None
            },
            {
                'ch': {
                    'name': '理财',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/money/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '保险',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/money/insurance/live.shtml',
                'ref': None
            },
            {
                'ch': {
                    'name': '宏观',
                    'count': 0
                },
                'url': 'http://finance.china.com.cn/news/index.shtml',
                'ref': None
            },
        ]

        # url = 'http://app.finance.china.com.cn/report/detail.php?id=4017056'
        # url = 'http://finance.china.com.cn/stock/qsdt/20120912/1013759.shtml'
        # url = 'http://finance.china.com.cn/money/fund/special/jjzk167/20150706/3213069.shtml'
        # url = 'http://www.china.com.cn/news/local/2013-06/20/content_29178516.htm'
        # url = 'http://news.china.com.cn/world/2018-01/02/content_50183456.htm'
        # url = 'http://local.china.com.cn/2013-07/02/content_29291539.htm'
        # url = 'http://news.china.com.cn/world/2018-01/03/content_50186120.htm'
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

        urls = response.xpath("//ul[@class='news_list']/li/a/@href | //ul[@id='c_list']/li/div[@class='c_title fl']/a/@href"
                              "| //div[@id='c1']/ul/li/a/@href").extract()
        for u in urls:
            u = urljoin(base, u)
            rcs.append({
                'ch': ch,
                'url': u,
                'ref': response.url
            })

        next_url = response.xpath("//a[text()='下一页']/@href | //a[text()='下页>>']/@href").extract_first()
        if next_url is not None:
            next_url = html.unescape(next_url)
            next_url = urljoin(base, next_url)
            nps.append({
                'ch': ch,
                'url': next_url,
                'ref': response.url
            })
        else:
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

        ls = response.css("#fontzoom>*:not(.fr.bianj):not(.ifa):not(#vf)").extract()
        if len(ls) < 1:
            ls = response.css(
                "#content>*:not(iframe):not(.mvdiv_1254085_holder):not(p:nth-last-child(1)[align='center'])").extract()
        if len(ls) < 1:
            ls = response.css("#articleBody>*:not(#vf):not(#autopage)").extract()
        if len(ls) < 1:
            ls = response.css("#artibody>*").extract()
        if len(ls) < 1:
            ls = response.xpath("//div[@class='p1']/p").extract()
        if len(ls) < 1:
            ls = response.css("#bigpic>*:not(#autopage)").extract()
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
            title = response.xpath("//div[@class='wrap c top']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='left_content']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//h1[@class='articleTitle']/text()").extract_first()
            if title is None:
                title = response.xpath("//h1[@id='artibodyTitle']/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='title_big']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//h1[@class='fb24']/text()").extract_first()
            if title is None:
                title = response.xpath("//h1[@class='tittle']/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@id='contit']/h1/text()").extract_first()
            item['title'] = title

            source = response.xpath("//span[@class='fl time2']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//span[@id='source_baidu']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//span[@id='source_baidu']/text()").re_first(r'来源：\s*(\S+)\s*')
            if source is None:
                source = response.xpath("//span[@class='fl time2']/text()").re_first(
                    r'[0-9]+年[0-9]+月[0-9]+日[0-9]+:[0-9]+\s+(\S+)\s*$')
            if source is None:
                source = response.xpath("//span[@id='art_source']/text()").extract_first()
            if source is None:
                source = response.xpath("//li[@class='small_one']/a[1]/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='con_left']/h3/text()").re_first(r'所属机构：(\S+)')
            if source is None:
                source = response.xpath("//table[@width='530']/tr/td[@width='270']/text()").re_first(r'文章来源:\s*(\S+)\s*')
            if source is None:
                source = response.xpath("//table[@width='530']/tr/td[@width='270']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='ly']/text()").re_first(r'文章来源:\s*(\S+)\s*')
            if source is not None:
                source = source.replace("china.com.cn", "")
            item["source"] = source

            pubtime = response.xpath("//span[@class='fl time2']/text()").re_first(
                r'([0-9]+年[0-9]+月[0-9]+日[0-9]+:[0-9]+)')
            if pubtime is None:
                pubtime = response.xpath("//span[@id='pubtime_baidu']/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//span[@id='pub_date']/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//li[@class='small_one']/span/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//h2[@class='gray1']/text()").re_first(r"报告日期：(\S+)")
            if pubtime is None:
                pubtime = response.xpath("//td[@align='center']/text()").re_first(r'\d+-\d+-\d+')
            if pubtime is None:
                pubtime = response.xpath("//div[@class='zrbj']/span/font/text()").re_first(r'\d+-\d+-\d+')
            if pubtime is not None:
                pubtime = pubtime.replace("发布时间：", "")
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日%H:%M')
                    pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
                item['pubtime'] = pubtime

            author = response.xpath("//span[@class='fl time2']/em/text()").extract_first()
            if author is None:
                author = response.xpath("//span[@id='author_baidu']/text()").extract_first()
            if author is None:
                author = response.xpath("//div[@class='con_left']/h3/text()").re_first(r"研究员：\s*(\S+)\s*所属机构")
            if author is not None:
                author = author.replace("作者：", "")
            item['author'] = author
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
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
