# -*- coding: utf-8 -*-

from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
import re
import json
from datetime import datetime


class CnfolNewsSpider(GGNewsSpider):
    name = 'News_Cnfol'
    sitename = '中金在线'
    allowed_domains = ['cnfol.com', 'app.cnfol.com', 'shell.cnfol.com']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(CnfolNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '财经-证券要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1591&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-头条精华',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1590&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '市场-市场测评',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1285&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '市场-股市聚焦',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1455&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '市场-主力动向',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4040&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '市场-板块聚焦',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4039&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '港股-A+H资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://hkstock.cnfol.com/A+Hzixun/index" + (
                    ('0' + str(pg)) if pg >= 2 else '') + ".shtml",
                'ref': None
            },
            {
                'ch': {
                    'name': '新闻频道-市场分析',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4057&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1') +
                                  "&end=10&pathurl=http://www.cnfol.hk/news/ganggujujiao/&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '新闻频道-即时市况',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4061&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/news/jishisk/&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '新闻频道-宏观财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4072&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/news/gncaijing/&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '新闻频道-新股要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4080&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/ipo/&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '沪深港通频道',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4071,4075,4076&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/shhkc/&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '新闻频道-窝轮要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4077,4078,4079&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/warrants/&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '基金-基金动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1302&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '基金-宏观经济',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=2025&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '私募频道-私募动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=2191&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '理财-债券资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4047&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货频道',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=133&starttime=1514509821&endtime=1514524221&num=30&page="
                                  + str(pg) + "&record=1&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-期市动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4108&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-机构论市',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1921&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-名家论市',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1615&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-金融期货',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4131&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-能源',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4133&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-化工',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4130&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '国际原油市场',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1816&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-农副',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4129&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '期货-金属',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4132&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '汇市观察',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1383&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '行业资讯',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=3579&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '汇市速递',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1381&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '专家汇评',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1504&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '机构分析',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1503&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '币种分析',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1382&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '外汇-外汇理财',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1507&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '外汇-二元期权',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=3574&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-产业经济',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1280&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-消费',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1603&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-IT',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1587&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '行业-行业综合',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1469&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '行业-商业',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1329&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '行业-行业数据',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1331&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '股票频道-行业',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/qualityarticles/Insurance_content_api.php?catid=124&limit=10&page="
                                  + str(pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-国内财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1277&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-商业要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1609&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '财经-国际财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1278&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '银行-银行业内动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1410&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '保险-保险动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1387&page=" + str(
                    pg) + "&callback=callback",
                'ref': None
            },
            {
                'ch': {
                    'name': '金市直播',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1710&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': None
            },
            {
                'ch': {
                    'name': '名家机构',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/dataapi/index.php/hotlable/selectArticle?keywords=%E5%90%8D%E5%AE%B6%E6%9C%BA%E6%9E%84&page="
                                  + str(pg) + "&num=10&type=%E5%A4%96%E6%B1%87&jsoncallback=",
                'ref': None
            },
        ]
        # url = 'http://sc.stock.cnfol.com/shichangjuejin/20171228/25831775.shtml'
        # url = 'http://hkstock.cnfol.com/A+Hzixun/20131030/16065440.shtml'
        # url = 'http://hkstock.cnfol.com/A+Hzixun/20131030/16064291.shtml'
        # url = 'http://hkstock.cnfol.com/A+Hzixun/20131031/16069401.shtml'
        # cp = cps[1]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_link(self, response):
        ch = response.meta['ch']
        pg = response.meta['pg']
        url = response.meta['url']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']
        if ch['name'] == '港股-A+H资讯':
            urls = response.xpath("//div[@class='Fl W640 LBar']/p/a/@href").extract()
        elif 'shell' in response.url:
            data = json.loads(response.text)['content']
            urls = [i['Url'] for i in data]
        elif ch['name'] == '名家机构':
            data = json.loads(response.text)
            urls = [i['Url'] for i in data]
        else:
            urls = re.findall(r'"Url":"(.*?)","CreatedTime"', response.text, re.S)
        for u in urls:
            u = u.replace("\\", "")
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
        ls = response.css('#Content>*:not(#showquote):not(#stocks):not(select), #Content::text').extract()
        if len(ls) < 1:
            ls = response.css(".Article>*, .Article::text").extract()
        if len(ls) < 1:
            ls = response.css("#__content>*:not(#editor_baidu), #__content::text").extract()
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

            title = response.xpath("//div[@class='Art NewArt']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//h3[@class='artTitle']/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='Art']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//h1[@id='Title']/text()").extract_first()
            if title is None:
                title = response.xpath("//h2[@id='Title']/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='EDArt']/h1/text()").extract_first()
            item["title"] = title

            pubtime = response.xpath("//span[@id='pubtime_baidu']/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//p[@class='Fl']/span[1]/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//div[@class='tit titV']/span[1]/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//div[@class='GSTitsL Cf']/span[1]/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//div[@class='tit']/span[1]/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//div[@class='artDes']/span/text()").re_first(
                    r'([0-9]+-[0-9]+-[0-9]+\s*[0-9]+:[0-9]+:[0-9]+)')
            if pubtime is None:
                pubtime = response.xpath("//div[@class='Subtitle']/text()").re_first(r'(\d+年\d+月\d+日\s*\d+:\d+)')
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日%H:%M')
                    pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
            item['pubtime'] = pubtime

            source = response.xpath("//div[@class='artDes']/span[2]/text()").re_first(r'来源[:|：](\S+)')
            if source is None:
                source = response.xpath(
                    "//span[@id='source_baidu']/a/text() | //span[@id='source_baidu']/span/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='Fl']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='Fl']/span/span/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='tit']/span/span/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='tit']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='tit titV']/span/span/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='tit titV']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='GSTitsL Cf']/span/span/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='GSTitsL Cf']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='Subtitle']/text()").re_first(
                    r'\d+年\d+月\d+日\s*\d+:\d+\s+(\S+)\s*')
            if source is None:
                source = response.xpath("//div[@class='Subtitle']/text()").re_first(
                    r'\d+年\d+月\d+日\s*\d+:\d+\s+(\S+)\s*\s+\s*')
            if source is not None:
                if 'K图' in source:
                    source = None
            item['source'] = source

            author = response.xpath("//span[@id='author_baidu']/text()").re_first(r"作者[:|：](\S+)")
            if author is None:
                author = response.xpath("//div[@class='artDes']/span/text()").re_first(r'作者[:|：](\S+)')
            if author is None:
                author = response.xpath("//p[@class='Fl']/span/text()").re_first(r'作者[:|：](\S+)')
            if author is None:
                author = response.xpath("//div[@class='tit titV']/span/text()").re_first(r'作者[:|：](\S+)')
            if author is None:
                author = response.xpath("//div[@class='tit']/span/text()").re_first(r'作者[:|：](\S+)')
            if author is None:
                author = response.xpath("//div[@class='GSTitsL Cf']/span/text()").re_first(r'作者[:|：](\S+)')
            item["author"] = author

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