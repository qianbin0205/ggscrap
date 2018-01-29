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
                    'entry': 'http://news.cnfol.com/zhengquanyaowen/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1591&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/zhengquanyaowen/'
            },
            {
                'ch': {
                    'name': '财经-头条精华',
                    'entry': 'http://news.cnfol.com/toutiaojinghua/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1590&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/toutiaojinghua/'
            },
            {
                'ch': {
                    'name': '市场-市场测评',
                    'entry': 'http://sc.stock.cnfol.com/shichangceping/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1285&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://sc.stock.cnfol.com/shichangceping/'
            },
            {
                'ch': {
                    'name': '市场-股市聚焦',
                    'entry': 'http://sc.stock.cnfol.com/gushijujiao/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1455&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://sc.stock.cnfol.com/gushijujiao/'
            },
            {
                'ch': {
                    'name': '市场-主力动向',
                    'entry': 'http://sc.stock.cnfol.com/zldongxiang/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4040&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://sc.stock.cnfol.com/zldongxiang/'
            },
            {
                'ch': {
                    'name': '市场-板块聚焦',
                    'entry': 'http://sc.stock.cnfol.com/bkjujiao/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4039&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://sc.stock.cnfol.com/bkjujiao/'
            },
            {
                'ch': {
                    'name': '港股-A+H资讯',
                    'entry': 'http://hkstock.cnfol.com/A+Hzixun/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://hkstock.cnfol.com/A+Hzixun/index" + (
                    ('0' + str(pg)) if pg >= 2 else '') + ".shtml",
                'ref': 'http://hkstock.cnfol.com/A+Hzixun/'
            },
            {
                'ch': {
                    'name': '新闻频道-市场分析',
                    'entry': 'http://www.cnfol.hk/news/ganggujujiao/',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4057&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1') +
                                  "&end=10&pathurl=http://www.cnfol.hk/news/ganggujujiao/&jsoncallback=",
                'ref': 'http://www.cnfol.hk/news/ganggujujiao/'
            },
            {
                'ch': {
                    'name': '新闻频道-即时市况',
                    'entry': 'http://www.cnfol.hk/news/jishisk/',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4061&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/news/jishisk/&jsoncallback=",
                'ref': 'http://www.cnfol.hk/news/jishisk/'
            },
            {
                'ch': {
                    'name': '新闻频道-宏观财经',
                    'entry': 'http://www.cnfol.hk/news/gncaijing/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4072&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/news/gncaijing/&jsoncallback=",
                'ref': 'http://www.cnfol.hk/news/gncaijing/'
            },
            {
                'ch': {
                    'name': '新闻频道-新股要闻',
                    'entry': 'http://www.cnfol.hk/ipo/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4080&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/ipo/&jsoncallback=",
                'ref': 'http://www.cnfol.hk/ipo/'
            },
            {
                'ch': {
                    'name': '沪深港通频道',
                    'entry': 'http://www.cnfol.hk/shhkc/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4071,4075,4076&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/shhkc/&jsoncallback=",
                'ref': 'http://www.cnfol.hk/shhkc/'
            },
            {
                'ch': {
                    'name': '新闻频道-窝轮要闻',
                    'entry': 'http://www.cnfol.hk/warrants/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://shell.cnfol.com/article/hk_article.php?classid=4077,4078,4079&start="
                                  + (str(pg * 10 + 1) if pg >= 1 else '1')
                                  + "&end=10&pathurl=http://www.cnfol.hk/warrants/&jsoncallback=",
                'ref': 'http://www.cnfol.hk/warrants/'
            },
            {
                'ch': {
                    'name': '基金-基金动态',
                    'entry': 'http://fund.cnfol.com/jijindongtai/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1302&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://fund.cnfol.com/jijindongtai/'
            },
            {
                'ch': {
                    'name': '基金-宏观经济',
                    'entry': 'http://fund.cnfol.com/hongguanjingji/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=2025&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://fund.cnfol.com/hongguanjingji/'
            },
            {
                'ch': {
                    'name': '私募频道-私募动态',
                    'entry': 'http://fund.cnfol.com/smjj/simudongtai/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=2191&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://fund.cnfol.com/smjj/simudongtai/'
            },
            {
                'ch': {
                    'name': '理财-债券资讯',
                    'entry': 'http://money.cnfol.com/zqzixun/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4047&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://money.cnfol.com/zqzixun/'
            },
            {
                'ch': {
                    'name': '期货频道',
                    'entry': 'http://futures.cnfol.com/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=133&starttime=1514509821&endtime=1514524221&num=30&page="
                                  + str(pg) + "&record=1&jsoncallback=",
                'ref': 'http://futures.cnfol.com/'
            },
            {
                'ch': {
                    'name': '期货-期市动态',
                    'entry': 'http://futures.cnfol.com/qishidongtai/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4108&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/qishidongtai/'
            },
            {
                'ch': {
                    'name': '期货-机构论市',
                    'entry': 'http://futures.cnfol.com/jigoulunshi/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1921&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/jigoulunshi/'
            },
            {
                'ch': {
                    'name': '期货-名家论市',
                    'entry': 'http://futures.cnfol.com/mingjialunshi/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1615&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/mingjialunshi/'
            },
            {
                'ch': {
                    'name': '期货-金融期货',
                    'entry': 'http://futures.cnfol.com/jinrongqihuo/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4131&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/jinrongqihuo/'
            },
            {
                'ch': {
                    'name': '期货-能源',
                    'entry': 'http://futures.cnfol.com/ny/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4133&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/ny/'
            },
            {
                'ch': {
                    'name': '期货-化工',
                    'entry': 'http://futures.cnfol.com/huagong/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4130&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/huagong/'
            },
            {
                'ch': {
                    'name': '国际原油市场',
                    'entry': 'http://gold.cnfol.com/guojiyuanyousc/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1816&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://gold.cnfol.com/guojiyuanyousc/'
            },
            {
                'ch': {
                    'name': '期货-农副',
                    'entry': 'http://futures.cnfol.com/nongfu/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4129&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/nongfu/'
            },
            {
                'ch': {
                    'name': '期货-金属',
                    'entry': 'http://futures.cnfol.com/js/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=4132&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://futures.cnfol.com/js/'
            },
            {
                'ch': {
                    'name': '汇市观察',
                    'entry': 'http://forex.cnfol.com/jingjiyaowen/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1383&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/jingjiyaowen/'
            },
            {
                'ch': {
                    'name': '行业资讯',
                    'entry': 'http://forex.cnfol.com/hyzx/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=3579&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/hyzx/'
            },
            {
                'ch': {
                    'name': '汇市速递',
                    'entry': 'http://forex.cnfol.com/huishizhibo/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1381&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/huishizhibo/'
            },
            {
                'ch': {
                    'name': '专家汇评',
                    'entry': 'http://forex.cnfol.com/zhuanjiajianyi/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1504&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/zhuanjiajianyi/'
            },
            {
                'ch': {
                    'name': '机构分析',
                    'entry': 'http://forex.cnfol.com/jigouhuiping/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1503&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/jigouhuiping/'
            },
            {
                'ch': {
                    'name': '币种分析',
                    'entry': 'http://forex.cnfol.com/bizhongfenxi/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1382&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/bizhongfenxi/'
            },
            {
                'ch': {
                    'name': '外汇-外汇理财',
                    'entry': 'http://forex.cnfol.com/waihuilicai/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1507&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/waihuilicai/'
            },
            {
                'ch': {
                    'name': '外汇-二元期权',
                    'entry': 'http://forex.cnfol.com/eyqq/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=3574&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://forex.cnfol.com/eyqq/'
            },
            {
                'ch': {
                    'name': '财经-产业经济',
                    'entry': 'http://news.cnfol.com/chanyejingji/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1280&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/chanyejingji/'
            },
            {
                'ch': {
                    'name': '财经-消费',
                    'entry': 'http://news.cnfol.com/xiaofei/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1603&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/xiaofei/'
            },
            {
                'ch': {
                    'name': '财经-IT',
                    'entry': 'http://news.cnfol.com/it/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1587&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/it/'
            },
            {
                'ch': {
                    'name': '行业-行业综合',
                    'entry': 'http://hy.stock.cnfol.com/hangyezonghe/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1469&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://hy.stock.cnfol.com/hangyezonghe/'
            },
            {
                'ch': {
                    'name': '行业-商业',
                    'entry': 'http://hy.stock.cnfol.com/bankuaijujiao/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1329&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://hy.stock.cnfol.com/bankuaijujiao/'
            },
            {
                'ch': {
                    'name': '行业-行业数据',
                    'entry': 'http://hy.stock.cnfol.com/hangyeshuju/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1331&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://hy.stock.cnfol.com/hangyeshuju/'
            },
            {
                'ch': {
                    'name': '股票频道-行业',
                    'entry': 'http://hy.stock.cnfol.com/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/qualityarticles/Insurance_content_api.php?catid=124&limit=10&page="
                                  + str(pg) + "&callback=",
                'ref': 'http://hy.stock.cnfol.com/'
            },
            {
                'ch': {
                    'name': '财经-国内财经',
                    'entry': 'http://news.cnfol.com/guoneicaijing/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1277&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/guoneicaijing/'
            },
            {
                'ch': {
                    'name': '财经-商业要闻',
                    'entry': 'http://news.cnfol.com/shangyeyaowen/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1609&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/shangyeyaowen/'
            },
            {
                'ch': {
                    'name': '财经-国际财经',
                    'entry': 'http://news.cnfol.com/guojicaijing/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1278&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://news.cnfol.com/guojicaijing/'
            },
            {
                'ch': {
                    'name': '银行-银行业内动态',
                    'entry': 'http://bank.cnfol.com/yinhangyeneidongtai/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1410&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://bank.cnfol.com/yinhangyeneidongtai/'
            },
            {
                'ch': {
                    'name': '保险-保险动态',
                    'entry': 'http://insurance.cnfol.com/baoxiandongtai/',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/test/newlist_api.php?catid=1387&page=" + str(
                    pg) + "&callback=",
                'ref': 'http://insurance.cnfol.com/baoxiandongtai/'
            },
            {
                'ch': {
                    'name': '金市直播',
                    'entry': 'http://gold.cnfol.com/jinshizhibo/',
                    'count': 0
                },
                'pg': 1,
                'url': "http://shell.cnfol.com/article/gold_article.php?classid=1710&title=&start=0&end=250&apikey=&jsoncallback=",
                'ref': 'http://gold.cnfol.com/jinshizhibo/'
            },
            {
                'ch': {
                    'name': '名家机构',
                    'entry': 'http://forex.cnfol.com/keyword/mjjg.shtml',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: "http://app.cnfol.com/dataapi/index.php/hotlable/selectArticle?keywords=%E5%90%8D%E5%AE%B6%E6%9C%BA%E6%9E%84&page="
                                  + str(pg) + "&num=10&type=%E5%A4%96%E6%B1%87&jsoncallback=",
                'ref': 'http://forex.cnfol.com/keyword/mjjg.shtml'
            },
        ]
        # url = 'http://sc.stock.cnfol.com/shichangjuejin/20171228/25831775.shtml'
        # url = 'http://hkstock.cnfol.com/A+Hzixun/20131030/16065440.shtml'
        # url = 'http://hkstock.cnfol.com/A+Hzixun/20131030/16064291.shtml'
        # url = 'http://hkstock.cnfol.com/A+Hzixun/20131031/16069401.shtml'
        # url = 'http://futures.cnfol.com/mingjialunshi/20180122/25932672.shtml'
        # url = 'http://gold.cnfol.com/guojiyuanyousc/20180122/25934538.shtml'
        # url = 'http://gold.cnfol.com/guojiyuanyousc/20180122/25933608.shtml'
        # url = 'http://gold.cnfol.com/guojiyuanyousc/20180123/25939136.shtml'
        # cp = cps[1]
        # yield self.request_next([], [{'ch': cp['ch'], 'url': url, 'ref': cp['ref']}], [])

        yield self.request_next(cps, [], [])

    def parse_list(self, response):
        ch = response.meta['ch']
        pg = response.meta['pg']
        url = response.meta['url']
        cps = response.meta['cps']
        ips = response.meta['ips']
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
            urls = re.findall(r'http:\\/\\/\w+.cnfol.com\\/\w+\\/\d+\\/\d+.shtml', response.text, re.S)
        for u in urls:
            u = u.replace("\\", "")
            ips.append({
                'ch': ch,
                'url': u,
                'ref': response.request.headers['Referer']
            })

        if urls:
            nps.append({
                'ch': ch,
                'pg': pg + 1,
                'url': url,
                'ref': response.request.headers['Referer']
            })

        yield self.request_next(cps, ips, nps)

    def parse_item(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        ips = response.meta['ips']
        nps = response.meta['nps']

        ext = response.meta['ext']
        ls = response.css('#Content>*:not(#showquote):not(#stocks):not(select), #Content::text').extract()
        if len(ls) < 1:
            ls = response.css(".Article>*, .Article::text").extract()
        if len(ls) < 1:
            ls = response.css("#__content>*:not(#editor_baidu), #__content::text").extract()
        if not ls:
            ls = response.css('.ArtDsc .content>*,.ArtDsc .content::text').extract()
        if not ls:
            ls = response.css('.EDArt>.EDArtInfo>*,.EDArt>.EDArtInfo::text').extract()
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
            if title is None:
                title = response.css('h1.ArtH1::text').extract_first()
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
            if pubtime is None:
                pubtime = response.css('.ArtHps>span').re_first(r'\d+-\d+-\d+\s*\d+:\d+:\d+')
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日%H:%M')
                else:
                    pubtime = datetime.strptime(pubtime, '%Y-%m-%d %H:%M:%S')
            item['pubtime'] = pubtime

            source = response.xpath("//div[@class='artDes']/span[2]/text()").re_first(r'来源[:|：](\S+)')
            if source is None:
                source = response.css('#tit>span>span>a::text').extract_first()
            if source is None:
                source = response.xpath(
                    "//span[@id='source_baidu']/a/text() | //span[@id='source_baidu']/span/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='Fl']/span/a/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='Fl']/span/span/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='tit']/span/span/span/text()").extract_first()
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
            if author is None:
                author = response.css('#tit>span>span').re_first(r'作者：(.+)<')
            item["author"] = author

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is None:
            yield item
            ch['count'] = ch['count'] + 1
        else:
            ips.insert(0, {
                'ch': ch,
                'url': next_url,
                'ref': response.url,
                'ext': {'item': item}
            })

        yield self.request_next(cps, ips, nps)
