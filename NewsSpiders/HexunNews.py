# -*- coding: utf-8 -*-

import config
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
from datetime import datetime
import json
import re


class HexunNewsSpider(GGNewsSpider):
    name = 'News_Hexun'
    sitename = '和讯网'
    allowed_domains = ['hexun.com']
    handle_httpstatus_list = [404]

    proxy = config.proxy

    start_urls = []
    cps = [
        {
            'ch': {
                'name': '新闻首页-公司新闻',
                'entry': 'http://news.hexun.com/listedcompany/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=108511812&priority=0&callback=',
            'ref': 'http://news.hexun.com/listedcompany/'
        },
        {
            'ch': {
                'name': '新股-新股申购中签',
                'entry': 'http://stock.hexun.com/shengou/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=100235875&priority=0&callback=',
            'ref': 'http://stock.hexun.com/shengou/'
        },
        {
            'ch': {
                'name': '新股-拟上市公司新闻',
                'entry': 'http://stock.hexun.com/nss/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=118806608&priority=0&callback=',
            'ref': 'http://stock.hexun.com/nss/'
        },
        {
            'ch': {
                'name': '港股-港股要闻',
                'entry': 'http://stock.hexun.com/ggyw/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=100852160&priority=0&callback=',
            'ref': 'http://stock.hexun.com/ggyw/'
        },
        {
            'ch': {
                'name': '基金要闻',
                'entry': 'http://funds.hexun.com/hotnews/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=102707162&priority=0&callback=',
            'ref': 'http://funds.hexun.com/hotnews/'
        },
        {
            'ch': {
                'name': '基金评论-基金市场评论',
                'entry': 'http://funds.hexun.com/fundmarket/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=102556523&priority=0&callback=',
            'ref': 'http://funds.hexun.com/fundmarket/'
        },
        {
            'ch': {
                'name': '基金评论-持仓分析',
                'entry': 'http://funds.hexun.com/store/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=102556539&priority=0&callback=',
            'ref': 'http://funds.hexun.com/store/'
        },
        {
            'ch': {
                'name': '债券新闻',
                'entry': 'http://bond.hexun.com/news/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101060457&priority=0&callback=',
            'ref': 'http://bond.hexun.com/news/'
        },
        {
            'ch': {
                'name': '债券-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=115',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=115&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=115'
        },
        {
            'ch': {
                'name': '债券公告',
                'entry': 'http://bond.hexun.com/tzgg/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101078261&priority=0&callback=',
            'ref': 'http://bond.hexun.com/tzgg/'
        },
        {
            'ch': {
                'name': '债市分析-海外及周边债市',
                'entry': 'http://bond.hexun.com/hwsc/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101077663&priority=0&callback=',
            'ref': 'http://bond.hexun.com/hwsc/'
        },
        {
            'ch': {
                'name': '期货-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=116',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=116&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=116'
        },
        {
            'ch': {
                'name': '股指期货要闻',
                'entry': 'http://qizhi.hexun.com/yaowen/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101757360&priority=0&callback=',
            'ref': 'http://qizhi.hexun.com/yaowen/'
        },
        {
            'ch': {
                'name': '股指期货-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=118',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=118&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=118'
        },
        {
            'ch': {
                'name': '期指市场日评',
                'entry': 'http://qizhi.hexun.com/qizhiriping/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=123619081&priority=0&callback=',
            'ref': 'http://qizhi.hexun.com/qizhiriping/'
        },
        {
            'ch': {
                'name': '股指期货研究报告',
                'entry': 'http://qizhi.hexun.com/gzqhyjbg/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=141026245&priority=0&callback=',
            'ref': 'http://qizhi.hexun.com/gzqhyjbg/'
        },
        {
            'ch': {
                'name': '国债期货评论',
                'entry': 'http://futures.hexun.com/gzqhpl/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=143082345&priority=0&callback=',
            'ref': 'http://futures.hexun.com/gzqhpl/'
        },
        {
            'ch': {
                'name': '股指期货杂谈',
                'entry': 'http://qizhi.hexun.com/guonei/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101757327&priority=0&callback=',
            'ref': 'http://qizhi.hexun.com/guonei/'
        },
        {
            'ch': {
                'name': '期货资讯-能源资讯',
                'entry': 'http://futures.hexun.com/nyzx/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=130519488&priority=0&callback=',
            'ref': 'http://futures.hexun.com/nyzx/'
        },
        {
            'ch': {
                'name': '期货资讯-化工资讯',
                'entry': 'http://futures.hexun.com/chemicalnews/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=130518597&priority=0&callback=',
            'ref': 'http://futures.hexun.com/chemicalnews/'
        },
        {
            'ch': {
                'name': '黄金首页-分析评论-能源市场',
                'entry': 'http://gold.hexun.com/energy/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=102182812&priority=0&callback=',
            'ref': 'http://gold.hexun.com/energy/'
        },
        {
            'ch': {
                'name': '期货资讯-农副资讯',
                'entry': 'http://futures.hexun.com/agriculturenews/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101065616&priority=0&callback=',
            'ref': 'http://futures.hexun.com/agriculturenews/'
        },
        {
            'ch': {
                'name': '期货资讯-金属资讯',
                'entry': 'http://futures.hexun.com/industrynews/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101065619&priority=0&callback=',
            'ref': 'http://futures.hexun.com/industrynews/'
        },
        {
            'ch': {
                'name': '外汇-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=107',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=107&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=107'
        },
        {
            'ch': {
                'name': '新闻首页-产业报道',
                'entry': 'http://news.hexun.com/company/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=100018983&priority=0&callback=',
            'ref': 'http://news.hexun.com/company/'
        },
        {
            'ch': {
                'name': '汽车-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=124',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=124&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=124'
        },
        {
            'ch': {
                'name': '房产-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=105',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=105&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=105'
        },
        {
            'ch': {
                'name': '时事要闻-国内时事',
                'entry': 'http://news.hexun.com/gnss/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=136147678&priority=0&callback=',
            'ref': 'http://news.hexun.com/gnss/'
        },
        {
            'ch': {
                'name': '时事要闻-国际时事',
                'entry': 'http://news.hexun.com/gjss/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=136147698&priority=0&callback=',
            'ref': 'http://news.hexun.com/gjss/'
        },
        {
            'ch': {
                'name': '美股市场-全球市场',
                'entry': 'http://stock.hexun.com/usdongtai/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=108532775&priority=0&callback=',
            'ref': 'http://stock.hexun.com/usdongtai/'
        },
        {
            'ch': {
                'name': '银行-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=121',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=121&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=121'
        },
        {
            'ch': {
                'name': '券商-证券公司',
                'entry': 'http://stock.hexun.com/qsdx/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=136571896&priority=0&callback=',
            'ref': 'http://stock.hexun.com/qsdx/'
        },
        {
            'ch': {
                'name': '券商-证券业动态',
                'entry': 'http://stock.hexun.com/jgdt/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=136572060&priority=0&callback=',
            'ref': 'http://stock.hexun.com/jgdt/'
        },
        {
            'ch': {
                'name': '黄金-滚动新闻',
                'entry': 'http://roll.hexun.com/?source=120',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=120&date='
                              + datetime.now().strftime('%Y-%m-%d') + '&page=' + str(pg),
            'ref': 'http://roll.hexun.com/?source=120'
        },
        {
            'ch': {
                'name': '最新资讯-金市动态',
                'entry': 'http://gold.hexun.com/market/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101790787&priority=0&callback=',
            'ref': 'http://gold.hexun.com/market/'
        },
        {
            'ch': {
                'name': '黄金首页-分析评论-海外及周边市场',
                'entry': 'http://gold.hexun.com/oversea/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101790968&priority=0&callback=',
            'ref': 'http://gold.hexun.com/oversea/'
        },
        {
            'ch': {
                'name': '白银频道-业内第一专业白银投资平台白银市场动态',
                'entry': 'http://gold.hexun.com/byscdt/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=132766830&priority=0&callback=',
            'ref': 'http://gold.hexun.com/byscdt/'
        },
        {
            'ch': {
                'name': '分析评论-每日金评',
                'entry': 'http://gold.hexun.com/comment/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101790947&priority=0&callback=',
            'ref': 'http://gold.hexun.com/comment/'
        },
        {
            'ch': {
                'name': '黄金首页-分析评论-深度剖析',
                'entry': 'http://gold.hexun.com/research/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=101790971&priority=0&callback=',
            'ref': 'http://gold.hexun.com/research/'
        },
        {
            'ch': {
                'name': '新闻首页-宏观经济',
                'entry': 'http://news.hexun.com/economy/',
                'count': 0
            },
            'pg': 1,
            'url': lambda pg: 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?s=30&cp=' + str(
                pg) + '&id=100018985&priority=0&callback=',
            'ref': 'http://news.hexun.com/economy/'
        },
        {
            'ch': {
                'name': '港股-中资股新闻',
                'entry': 'http://stock.hexun.com/zzg/',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://stock.hexun.com/zzg/index'
                              + (('-' + str(202 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://stock.hexun.com/zzg/'
        },
        {
            'ch': {
                'name': '港股-香港新股再融资',
                'entry': 'http://stock.hexun.com/xg/',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://stock.hexun.com/xg/index'
                              + (('-' + str(56 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://stock.hexun.com/xg/'
        },
        {
            'ch': {
                'name': '港股-券商动向',
                'entry': 'http://hk.stock.hexun.com/ggqsdx/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://hk.stock.hexun.com/ggqsdx/index'
                              + (('-' + str(10 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://hk.stock.hexun.com/ggqsdx/index.html'
        },
        {
            'ch': {
                'name': '美股市场-国际市场评论',
                'entry': 'http://stock.hexun.com/wjscpl/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://stock.hexun.com/wjscpl/index'
                              + (('-' + str(14 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://stock.hexun.com/wjscpl/index.html'
        },
        {
            'ch': {
                'name': ' 美股市场-美股公司新闻',
                'entry': 'http://stock.hexun.com/mggi/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://stock.hexun.com/mggi/index'
                              + (('-' + str(414 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://stock.hexun.com/mggi/index.html'
        },
        {
            'ch': {
                'name': '美股市场-中国概念股播报',
                'entry': 'http://stock.hexun.com/gainiangu/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://stock.hexun.com/gainiangu/index'
                              + (('-' + str(96 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://stock.hexun.com/gainiangu/index.html'
        },
        {
            'ch': {
                'name': '国债-国债动态',
                'entry': 'http://bond.hexun.com/gzdt/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://bond.hexun.com/gzdt/index'
                              + (('-' + str(188 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://bond.hexun.com/gzdt/index.html'
        },
        {
            'ch': {
                'name': '可转债-可转债动态',
                'entry': 'http://bond.hexun.com/kzzdt/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://bond.hexun.com/kzzdt/index'
                              + (('-' + str(15 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://bond.hexun.com/kzzdt/index.html'
        },
        {
            'ch': {
                'name': '债市分析-交易所债市',
                'entry': 'http://bond.hexun.com/jyssc/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://bond.hexun.com/jyssc/index'
                              + (('-' + str(84 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://bond.hexun.com/jyssc/index.html'
        },
        {
            'ch': {
                'name': '债市分析-银行间债市',
                'entry': 'http://bond.hexun.com/yhjsc/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://bond.hexun.com/yhjsc/index'
                              + (('-' + str(112 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://bond.hexun.com/yhjsc/index.html'
        },
        {
            'ch': {
                'name': '和债市分析-债市研究',
                'entry': 'http://bond.hexun.com/sdyj/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://bond.hexun.com/sdyj/index'
                              + (('-' + str(228 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://bond.hexun.com/sdyj/index.html'
        },
        {
            'ch': {
                'name': '债券首页-地方债',
                'entry': 'http://bond.hexun.com/dfz/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://bond.hexun.com/dfz/index'
                              + (('-' + str(pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://bond.hexun.com/dfz/index.html'
        },
        {
            'ch': {
                'name': '期货资讯-环球市场资讯',
                'entry': 'http://futures.hexun.com/jwysp/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://futures.hexun.com/jwysp/index'
                              + (('-' + str(316 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://futures.hexun.com/jwysp/index.html'
        },
        {
            'ch': {
                'name': '期货资讯-期货行业资讯',
                'entry': 'http://futures.hexun.com/integratednews/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://futures.hexun.com/integratednews/index'
                              + (('-' + str(115 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://futures.hexun.com/integratednews/index.html'
        },
        {
            'ch': {
                'name': '期货分析评论-期货操作建议',
                'entry': 'http://futures.hexun.com/domestic/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://futures.hexun.com/domestic/index'
                              + (('-' + str(134 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://futures.hexun.com/domestic/index.html'
        },
        {
            'ch': {
                'name': '期货分析评论-期货焦点透视',
                'entry': 'http://futures.hexun.com/focus/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://futures.hexun.com/focus/index'
                              + (('-' + str(103 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://futures.hexun.com/focus/index.html'
        },
        {
            'ch': {
                'name': '股指期货首页-名家论市',
                'entry': 'http://qizhi.hexun.com/qzmj/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://qizhi.hexun.com/qzmj/index'
                              + (('-' + str(246 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://qizhi.hexun.com/qzmj/index.html'
        },
        {
            'ch': {
                'name': '股指期货国内评论',
                'entry': 'http://qizhi.hexun.com/guoneiping/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://qizhi.hexun.com/guoneiping/index'
                              + (('-' + str(678 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://qizhi.hexun.com/guoneiping/index.html'
        },
        {
            'ch': {
                'name': '期货首页- 期权',
                'entry': 'http://futures.hexun.com/option/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://futures.hexun.com/option/index'
                              + (('-' + str(56 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://futures.hexun.com/option/index.html'
        },
        {
            'ch': {
                'name': '外汇新闻-汇市观察',
                'entry': 'http://forex.hexun.com/fxobservation/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/fxobservation/index'
                              + (('-' + str(1266 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/fxobservation/index.html'
        },
        {
            'ch': {
                'name': '外汇新闻-市场资讯',
                'entry': 'http://forex.hexun.com/market/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/market/index'
                              + (('-' + str(6584 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/market/index.html'
        },
        {
            'ch': {
                'name': '外汇首页-币种专栏',
                'entry': 'http://forex.hexun.com/currency/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/currency/index'
                              + (('-' + str(1184 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/currency/index.html'
        },
        {
            'ch': {
                'name': '人民币频道-人民币要闻',
                'entry': 'http://forex.hexun.com/rmbhotnews/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/rmbhotnews/index'
                              + (('-' + str(90 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/rmbhotnews/index.html'
        },
        {
            'ch': {
                'name': '人民币频道-离岸市场',
                'entry': 'http://forex.hexun.com/lian/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/lian/index'
                              + (('-' + str(7 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/lian/index.html'
        },
        {
            'ch': {
                'name': '人民币频道-跨境结算',
                'entry': 'http://forex.hexun.com/kuajing/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/kuajing/index'
                              + (('-' + str(pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/kuajing/index.html'
        },
        {
            'ch': {
                'name': '人民币频道-政策动态',
                'entry': 'http://forex.hexun.com/zhengce/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/zhengce/index'
                              + (('-' + str(6 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/zhengce/index.html'
        },
        {
            'ch': {
                'name': '人民币频道-大行研报',
                'entry': 'http://forex.hexun.com/yanbao/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/yanbao/index'
                              + (('-' + str(11 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/yanbao/index.html'
        },
        {
            'ch': {
                'name': '外汇首页-外汇公司',
                'entry': 'http://forex.hexun.com/brokernews/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/brokernews/index'
                              + (('-' + str(33 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/brokernews/index.html'
        },
        {
            'ch': {
                'name': '外汇分析-机构分析',
                'entry': 'http://forex.hexun.com/institution/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/institution/index'
                              + (('-' + str(2545 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/institution/index.html'
        },
        {
            'ch': {
                'name': '外汇新闻-深度分析',
                'entry': 'http://forex.hexun.com/opinion/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://forex.hexun.com/opinion/index'
                              + (('-' + str(239 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://forex.hexun.com/opinion/index.html'
        },
        {
            'ch': {
                'name': '汽车产业资讯-汽车要闻',
                'entry': 'http://auto.hexun.com/qcyw/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://auto.hexun.com/qcyw/index'
                              + (('-' + str(3360 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://auto.hexun.com/qcyw/index.html'
        },
        {
            'ch': {
                'name': '汽车产业资讯-车企动态',
                'entry': 'http://auto.hexun.com/cheqidt/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://auto.hexun.com/cheqidt/index'
                              + (('-' + str(196 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://auto.hexun.com/cheqidt/index.html'
        },

        {
            'ch': {
                'name': '科技首页-科技要闻',
                'entry': 'http://tech.hexun.com/highlights/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://tech.hexun.com/highlights/index'
                              + (('-' + str(14550 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://tech.hexun.com/highlights/index.html'
        },
        {
            'ch': {
                'name': '保险首页-今日导读',
                'entry': 'http://insurance.hexun.com/bxjrdd/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxjrdd/index'
                              + (('-' + str(491 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxjrdd/index.html'
        },
        {
            'ch': {
                'name': '保险首页-业内资讯-行业资讯',
                'entry': 'http://insurance.hexun.com/bxhyzx/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxhyzx/index'
                              + (('-' + str(519 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxhyzx/index.html'
        },
        {
            'ch': {
                'name': '保险首页-业内资讯-公司新闻',
                'entry': 'http://insurance.hexun.com/bxgsxw/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxgsxw/index'
                              + (('-' + str(584 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxgsxw/index.html'
        },
        {
            'ch': {
                'name': '保险首页-业内资讯-监管动态',
                'entry': 'http://insurance.hexun.com/bxjgdt/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxjgdt/index'
                              + (('-' + str(206 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxjgdt/index.html'
        },
        {
            'ch': {
                'name': '保险首页-业内资讯-评论与研究',
                'entry': 'http://insurance.hexun.com/bxscpl/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxscpl/index'
                              + (('-' + str(158 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxscpl/index.html'
        },
        {
            'ch': {
                'name': '保险首页-业内资讯-营销动态',
                'entry': 'http://insurance.hexun.com/bxyxdt/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxyxdt/index'
                              + (('-' + str(135 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxyxdt/index.html'
        },
        {
            'ch': {
                'name': '保险首页-业内资讯-保险人物',
                'entry': 'http://insurance.hexun.com/bxrw/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://insurance.hexun.com/bxrw/index'
                              + (('-' + str(129 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://insurance.hexun.com/bxrw/index.html'
        },
        {
            'ch': {
                'name': '信托行业动态',
                'entry': 'http://trust.hexun.com/trust_industry/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://trust.hexun.com/trust_industry/index'
                              + (('-' + str(497 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://trust.hexun.com/trust_industry/index.html'
        },
        {
            'ch': {
                'name': '信托研究',
                'entry': 'http://trust.hexun.com/trust_research/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://trust.hexun.com/trust_research/index'
                              + (('-' + str(34 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://trust.hexun.com/trust_research/index.html'
        },
        {
            'ch': {
                'name': '信托产品新闻',
                'entry': 'http://trust.hexun.com/trust_products/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://trust.hexun.com/trust_products/index'
                              + (('-' + str(11 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://trust.hexun.com/trust_products/index.html'
        },
        {
            'ch': {
                'name': '信托公司新闻',
                'entry': 'http://trust.hexun.com/trust_company/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://trust.hexun.com/trust_company/index'
                              + (('-' + str(82 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://trust.hexun.com/trust_company/index.html'
        },
        {
            'ch': {
                'name': '信托视点',
                'entry': 'http://trust.hexun.com/trustview/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://trust.hexun.com/trustview/index'
                              + (('-' + str(8 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://trust.hexun.com/trustview/index.html'
        },
        {
            'ch': {
                'name': '信托要闻',
                'entry': 'http://trust.hexun.com/xtyw/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://trust.hexun.com/xtyw/index'
                              + (('-' + str(135 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://trust.hexun.com/xtyw/index.html'
        },
        {
            'ch': {
                'name': '券商-券商人物',
                'entry': 'http://stock.hexun.com/qsrw/index.html',
                'count': 0
            },
            'pg': 0,
            'url': lambda pg: 'http://stock.hexun.com/qsrw/index'
                              + (('-' + str(5 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://stock.hexun.com/qsrw/index.html'
        },
        {
            'ch': {
                'name': '黄金机构',
                'entry': 'http://gold.hexun.com/goldinstitution/index.html',
                'count': 0,
            },
            'pg': 0,
            'url': lambda pg: 'http://gold.hexun.com/goldinstitution/index'
                              + (('-' + str(832 - pg)) if pg >= 1 else '') + '.html',
            'ref': 'http://gold.hexun.com/goldinstitution/index.html'
        },
    ]

    # url = 'http://hk.stock.hexun.com/2013-07-04/155777688.html'
    # url = 'http://hk.stock.hexun.com/2017-11-22/191737335.html'
    # url = 'http://stock.hexun.com/2007-06-15/100684360.html'
    # url = 'http://stock.hexun.com/2010-08-06/124502994.html'
    # url = 'http://futures.hexun.com/2017-12-25/192074489.html'
    # url = 'http://hk.stock.hexun.com/2014-05-03/164441425.html'
    # url = 'http://stock.hexun.com/2018-01-02/192138769.html'
    # cp = cps[0]
    # ips = [
    #     {
    #         'ch': cp['ch'],
    #         'url': url,
    #         'ref': cp['ref']
    #     },
    # ]

    def __init__(self, limit=None, *args, **kwargs):
        super(HexunNewsSpider, self).__init__(limit, *args, **kwargs)

    def parse_list(self, response):
        ch = response.meta['ch']
        pg = response.meta['pg']
        url = response.meta['url']

        base = get_base_url(response)

        if 'roll.hexun.com' in response.url:
            urls = re.findall(r"titleLink:'(.*?)',desc", response.text, re.S)
        elif 'index' in response.url:
            urls = response.xpath(
                "//div[@class='temp01']/ul/li/a/@href | //div[@id='zx1615']/ul/li/a/@href | //div[@class='mainbox']/ul/li/a/@href | //div[@class='lbcon']/ul/li/a/@href | //ul[@id='news_list']/li/a/@href").extract()
        else:
            data = json.loads(response.text)['result']
            urls = [i["entityurl"] for i in data]
        for u in urls:
            u = urljoin(base, u)
            self.ips.append({
                'ch': ch,
                'url': u,
                'ref': response.request.headers['Referer']
            })
        self.nps.append({
            'ch': ch,
            'pg': pg + 1,
            'url': url,
            'ref': response.request.headers['Referer']
        })

        yield self.request_next()

    def parse_item(self, response):
        ch = response.meta['ch']
        if '.html' not in response.url:
            pass
        elif response.url == 'http://forex.hexun.com/rmbzx/index.html':
            pass
        else:
            item = GGNewsItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['entry'] = ch['entry']
            item['url'] = response.url

            title = response.xpath("//div[@class='layout mg articleName']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@id='artibodyTitle']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//p[@class='blackbig']/text()").extract_first()
            item['title'] = title

            pubtime = response.xpath("//div[@class='tip fl']/span/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//span[@id='pubtime_baidu']/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//span[@id='artibodyDesc']/span[1]/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//div[@class='a']/span[1]/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//div[@class='from']/span[1]/text()").re_first(r'(\d+年\d+月\d+日\s*\d+:\d+)')
            if pubtime is None:
                pubtime = response.xpath("//div[@class='de_blue']/font/text()").extract_first()
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日%H:%M')
                else:
                    pubtime = datetime.strptime(pubtime, '%Y-%m-%d %H:%M:%S')
            item['pubtime'] = pubtime

            source = response.xpath("//div[@class='tip fl']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//span[@id='source_baidu']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//span[@id='source_baidu']/text()").re_first(r'来源：(\S+)')
            if source is None:
                source = response.xpath("//span[@id='artibodyDesc']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//span[@id='artibodyDesc']/text()").re_first(r'\S+')
            if source is None:
                source = response.xpath("//div[@class='from']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='author']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='author gray']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='tip fl']/text()").re_first(r'\S+')
            item['source'] = source

            author = response.xpath("//span[@id='author_baidu']/font/text()").extract_first()
            if author is None:
                author = response.xpath("//span[@class='gray']/font/text()").extract_first()
            if author is None:
                author = response.xpath("//div[@class='de_blue']/text()").re_first(r'作者：\s*(\S+)\s*')
            if author is None:
                author = response.xpath("//div[@class='author']/text()").re_first(r'作者：\s*(\S+)\s*来源')
            item["author"] = author

            ls = response.css(
                '.art_contextBox>*:not(:nth-last-child(1)):not(.showAll):not(.author):not(hexunnocommandread), .art_contextBox::text').extract()
            if len(ls) < 1:
                ls = response.css(
                    '.art_context>*:not(:nth-last-child(1)):not(.showAll):not(.author):not(hexunnocommandread):not(#stockSelectBox):not(.shareBox):not(#arctTailMark), .art_context::text').extract()
            if len(ls) < 1:
                ls = response.css(
                    '#artibody>*:not(:nth-last-child(1)):not(.showAll):not(.author):not(.btnlist):not(#yued):not(.clear):not(hexunnocommandread):not(#bqshengming20070928), #artibody::text').extract()
            if len(ls) < 1:
                ls = response.css(".detail_cnt>*, .detail_cnt::text").extract()
            content = ''.join(ls)
            item['content'] = content
            yield item

            ch['count'] = ch['count'] + 1

        yield self.request_next()
