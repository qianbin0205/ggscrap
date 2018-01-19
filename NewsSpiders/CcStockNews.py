# -*- coding: utf-8 -*-

import html
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider


class CcStockNewsSpider(GGNewsSpider):
    name = 'News_Ccstock'
    sitename = '中国资本证券网'
    allowed_domains = ['ccstock.cn']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(CcStockNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '股票频道-最新播报',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/zuixinbobao/',
                'ref': 'http://www.ccstock.cn/stock/zuixinbobao/'
            },
            {
                'ch': {
                    'name': '股票频道-公司评级',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/gongsipingji/',
                'ref': 'http://www.ccstock.cn/stock/gongsipingji/'
            },
            {
                'ch': {
                    'name': '股票频道-公司研究',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/gongsiyanjiu/',
                'ref': 'http://www.ccstock.cn/stock/gongsiyanjiu/'
            },
            {
                'ch': {
                    'name': '新股频道-新股公告',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/ipo/xingugonggao/',
                'ref': 'http://www.ccstock.cn/ipo/xingugonggao/'
            },
            {
                'ch': {
                    'name': '新股频道-新股评论',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/ipo/xingupinglun/',
                'ref': 'http://www.ccstock.cn/ipo/xingupinglun/'
            },
            {
                'ch': {
                    'name': '新股频道-上市预测',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/ipo/shangshiyuce/',
                'ref': 'http://www.ccstock.cn/ipo/shangshiyuce/'
            },
            {
                'ch': {
                    'name': '新股频道-申购指南',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/ipo/shengouzhinan/',
                'ref': 'http://www.ccstock.cn/ipo/shengouzhinan/'
            },
            {
                'ch': {
                    'name': '新股频道-申购中签',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/ipo/xinguzhongqian/',
                'ref': 'http://www.ccstock.cn/ipo/xinguzhongqian/'
            },
            {
                'ch': {
                    'name': '评论频道-商业评论',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/review/shangyepinglun/',
                'ref': 'http://www.ccstock.cn/review/shangyepinglun/'
            },
            {
                'ch': {
                    'name': '股票频道-港股市场分析	',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/HKstock/ganggufenxi/',
                'ref': 'http://www.ccstock.cn/HKstock/ganggufenxi/'
            },
            {
                'ch': {
                    'name': '美股频道',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/usstock/',
                'ref': 'http://www.ccstock.cn/usstock/'
            },
            {
                'ch': {
                    'name': '基金频道-基金动态',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/fund/jijindongtai/',
                'ref': 'http://www.ccstock.cn/fund/jijindongtai/'
            },
            {
                'ch': {
                    'name': '基金频道-基金论市',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/fund/jijinlunshi/',
                'ref': 'http://www.ccstock.cn/fund/jijinlunshi/'
            },
            {
                'ch': {
                    'name': '基金频道-持仓动向',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/fund/chicangdongxiang/',
                'ref': 'http://www.ccstock.cn/fund/chicangdongxiang/'
            },
            {
                'ch': {
                    'name': '基金频道-基金点评',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/fund/jijindiaoping/',
                'ref': 'http://www.ccstock.cn/fund/jijindiaoping/'
            },
            {
                'ch': {
                    'name': '私募频道-私募持仓',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/simu/chicang/',
                'ref': 'http://www.ccstock.cn/simu/chicang/'
            },
            {
                'ch': {
                    'name': '私募频道-私募论市',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/simu/lunshi/',
                'ref': 'http://www.ccstock.cn/simu/lunshi/'
            },
            {
                'ch': {
                    'name': '私募频道-私募动态',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/simu/dongtai/',
                'ref': 'http://www.ccstock.cn/simu/dongtai/'
            },
            {
                'ch': {
                    'name': '基金频道-基金经理访谈',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/fund/jijinfangtan/',
                'ref': 'http://www.ccstock.cn/fund/jijinfangtan/'
            },
            {
                'ch': {
                    'name': '理财频道-期货',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/money/qihuo/',
                'ref': 'http://www.ccstock.cn/money/qihuo/'
            },
            {
                'ch': {
                    'name': '理财频道-外汇',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/money/waihui/',
                'ref': 'http://www.ccstock.cn/money/waihui/'
            },
            {
                'ch': {
                    'name': '股票频道-行业研究',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/hangyeyanjiu/',
                'ref': 'http://www.ccstock.cn/stock/hangyeyanjiu/'
            },
            {
                'ch': {
                    'name': '股票频道-市场研究',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/shichangyanjiu/',
                'ref': 'http://www.ccstock.cn/stock/shichangyanjiu/'
            },
            {
                'ch': {
                    'name': '汽车频道-原创新闻',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/auto/qicheyuanchuang/index.html',
                'ref': 'http://www.ccstock.cn/auto/qicheyuanchuang/index.html'
            },
            {
                'ch': {
                    'name': '股票频道-环球股市',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/huanqiugushi/',
                'ref': 'http://www.ccstock.cn/stock/huanqiugushi/'
            },
            {
                'ch': {
                    'name': '财经频道-国际要闻',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/finance/guojijingji/',
                'ref': 'http://www.ccstock.cn/finance/guojijingji/'
            },
            {
                'ch': {
                    'name': '评论频道-国际聚焦',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/review/guojijujiao/',
                'ref': 'http://www.ccstock.cn/review/guojijujiao/'
            },
            {
                'ch': {
                    'name': '股票频道-银行',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/bank/',
                'ref': 'http://www.ccstock.cn/stock/bank/'
            },
            {
                'ch': {
                    'name': '理财频道-理财',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/money/licai/',
                'ref': 'http://www.ccstock.cn/money/licai/'
            },
            {
                'ch': {
                    'name': '股票频道-保险',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/insurance/',
                'ref': 'http://www.ccstock.cn/stock/insurance/'
            },
            {
                'ch': {
                    'name': '股票频道-信托',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/xintuo/',
                'ref': 'http://www.ccstock.cn/stock/xintuo/'
            },
            {
                'ch': {
                    'name': '股票频道-券商',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/stock/quanshang/',
                'ref': 'http://www.ccstock.cn/stock/quanshang/'
            },
            {
                'ch': {
                    'name': '股票频道-黄金',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/money/gold/',
                'ref': 'http://www.ccstock.cn/money/gold/'
            },
            {
                'ch': {
                    'name': '财经频道-宏观经济',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/finance/hongguanjingji/',
                'ref': 'http://www.ccstock.cn/finance/hongguanjingji/'
            },
            {
                'ch': {
                    'name': '评论频道-宏观时评',
                    'count': 0
                },
                'url': 'http://www.ccstock.cn/review/hongguanshiping/',
                'ref': 'http://www.ccstock.cn/review/hongguanshiping/'
            },

        ]

        # url = 'http://www.ccstock.cn/stock/redian/2017-12-08/A1512702491581.html'
        # url = 'http://www.ccstock.cn/gscy/gongsi/2017-12-13/A1513154340826.html'
        # url = 'http://www.ccstock.cn/stock/gegupinglun/2017-07-27/A1501113177689.html'
        # url = 'http://www.ccstock.cn/ipo/xingupinglun/2013-03-27/A1123549.html'
        # cp = cps[2]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_link(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']

        if response.status == 404:
            pass
        else:
            base = get_base_url(response)

            urls = response.xpath(
                "//div[@class='listMain']/ul/li/a/@href|//div[@class='list-left left']/ul/li/a/@href").extract()
            for url in urls:
                url = urljoin(base, url)
                rcs.append({
                    'ch': ch,
                    'url': url,
                    'ref': response.url
                })

            url = response.xpath("//a[text()='下一页']/@href").extract_first()
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
        ls = response.css(
            "#newscontent>*:not(p[align='center']):not(.pagebox):not(iframe), #newscontent::text").extract()
        if len(ls) < 1:
            ls = response.css(".content>*, .content::text").extract()
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
            title = response.xpath("//div[@class='bt']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='news_content']/h1/text()").extract_first()
            item['title'] = title
            source = response.xpath("//div[@class='sub_bt']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='sub_bt']/span/text()").re_first(r"^文章来源：(\S.*\S)\s+更新时间：")
            if source is None:
                source = response.xpath("//div[@class='info_news']/text()").re_first(r"^文章来源：(\S.*\S)\s+更新时间：")
            item['source'] = source

            pubtime = response.xpath("//div[@class='sub_bt']/span/text()").re_first(r"\d+-\d+-\d+\s*\d+:\d+")
            if pubtime is None:
                pubtime = response.xpath("//div[@class='info_news']/text()").re_first(r"\d+-\d+-\d+\s*\d+:\d+")
            item['pubtime'] = pubtime

            item["author"] = response.xpath("//span[@class='author']/text()").re_first("\s+\((\S+)\)\s+")

        next_url = response.xpath("//span[@class='next']/a/@href").extract_first()
        if next_url is not None:
            rcs.insert(0, {
                'ch': ch,
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url,
                'ext': {'item': item}
            })
        else:
            yield item

            ch['count'] = ch['count'] + 1

        yield self.request_next(cps, rcs, nps)
