# -*- coding: utf-8 -*-

import re
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
from datetime import timedelta, date
from datetime import datetime


class JrjNewsSpider(GGNewsSpider):
    name = 'News_Jrj'
    sitename = '金融界'
    allowed_domains = ['jrj.com.cn']
    start_urls = []

    handle_httpstatus_list = [404]

    def __init__(self, limit=None, *args, **kwargs):
        super(JrjNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '股票频道-宏观参考',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/invest/hgck' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/invest/hgck.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-市况直击',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://stock.jrj.com.cn/skzj/skzj' + date.isoformat(
                    date.today() - timedelta(days=pg)) + '.js',
                'ref': 'http://stock.jrj.com.cn/skzj/'
            },
            {
                'ch': {
                    'name': '7*24小时上市公司新闻',
                    'count': 0
                },
                'pg': 0,
                'url': lambda pg: 'http://stock.jrj.com.cn/share/news/company/' + date.isoformat(
                    date.today() - timedelta(days=pg)) + '.js',
                'ref': 'http://stock.jrj.com.cn/company/'
            },
            {
                'ch': {
                    'name': '股票频道-带你读研报',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/list/dndyb' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/list/dndyb.shtml'
            },
            {
                'ch': {
                    'name': '特殊资讯数据-机会早知道',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/share/news/qingbao/' + date.isoformat(
                    date.today() - timedelta(days=pg)) + '.js',
                'ref': 'http://stock.jrj.com.cn/jhqb/jhqb.shtml'
            },
            {
                'ch': {
                    'name': '特色资讯数据-涨跌停揭秘',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/share/news/zhangting/' + date.isoformat(
                    date.today() - timedelta(days=pg)) + '.js',
                'ref': 'http://stock.jrj.com.cn/ztbjm/ztbjm.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-新股要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/ipo/ipoxgyw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/ipo/ipoxgyw.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-新股策略',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/ipo/ipotzjq' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/ipo/ipotzjq.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-新股申购中签',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/ipo/xgsgzq' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/ipo/xgsgzq.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-再融资动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/ipo/zrzdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/ipo/zrzdt.shtml'
            },
            {
                'ch': {
                    'name': '港股频道-滚动资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://hk.jrj.com.cn/list/gdxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://hk.jrj.com.cn/list/gdxw.shtml'
            },
            {
                'ch': {
                    'name': '港股频道-操盘必读',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://hk.jrj.com.cn/list/cpbd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://hk.jrj.com.cn/list/cpbd.shtml'
            },
            {
                'ch': {
                    'name': '港股频道-研究分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://hk.jrj.com.cn/list/yjfx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://hk.jrj.com.cn/list/yjfx.shtml'
            },
            {
                'ch': {
                    'name': '港股频道-窝轮/牛熊证',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://hk.jrj.com.cn/list/wlnxz' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://hk.jrj.com.cn/list/wlnxz.shtml'
            },
            {
                'ch': {
                    'name': '港股频道-专家股评',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://hk.jrj.com.cn/list/mjzl' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://hk.jrj.com.cn/list/mjzl.shtml'
            },
            {
                'ch': {
                    'name': '美股频道-美股要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://usstock.jrj.com.cn/list/mgyw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://usstock.jrj.com.cn/list/mgyw.shtml'
            },
            {
                'ch': {
                    'name': '美股频道-美股滚动',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://usstock.jrj.com.cn/list/mggd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://usstock.jrj.com.cn/list/mggd.shtml'
            },
            {
                'ch': {
                    'name': '美股频道-中国概念股',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://usstock.jrj.com.cn/list/zggng' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://usstock.jrj.com.cn/list/zggng.shtml'
            },
            {
                'ch': {
                    'name': '美股频道-研究分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://usstock.jrj.com.cn/list/yjfx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://usstock.jrj.com.cn/list/yjfx.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-股市资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/list/stockgszx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/list/stockgszx.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/jjgd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/jjgd.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-基金动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/jjdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/jjdt.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-社保基金',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/sbjj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/sbjj.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-QDII',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/qdii' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/qdii.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-QFII',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/qfii' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/qfii.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-基金看市',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/jjks' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/jjks.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-基金原创',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/yc' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/yc.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-海外基金',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/hwjj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/hwjj.shtml'
            },
            {
                'ch': {
                    'name': '基金频道-基金研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://fund.jrj.com.cn/list/plyj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://fund.jrj.com.cn/list/plyj.shtml'
            },
            {
                'ch': {
                    'name': '私募基金-滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://simu.jrj.com.cn/list/gdxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://simu.jrj.com.cn/list/gdxw.shtml'
            },
            {
                'ch': {
                    'name': '私募基金-私募动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://simu.jrj.com.cn/list/smdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://simu.jrj.com.cn/list/smdt.shtml'
            },
            {
                'ch': {
                    'name': '私募基金-私募观点',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://simu.jrj.com.cn/list/smgd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://simu.jrj.com.cn/list/smgd.shtml'
            },
            {
                'ch': {
                    'name': '私募基金-私募人物',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://simu.jrj.com.cn/list/smrw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://simu.jrj.com.cn/list/smrw.shtml'
            },
            {
                'ch': {
                    'name': '私募基金-私募访谈',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://simu.jrj.com.cn/list/smft' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://simu.jrj.com.cn/list/smft.shtml'
            },
            {
                'ch': {
                    'name': '债券频道-滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bond.jrj.com.cn/list/zqgdxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bond.jrj.com.cn/list/zqgdxw.shtml'
            },
            {
                'ch': {
                    'name': '债券频道-债券资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bond.jrj.com.cn/list/zqzx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bond.jrj.com.cn/list/zqzx.shtml'
            },
            {
                'ch': {
                    'name': '债券频道-新发债券',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bond.jrj.com.cn/list/xfzq' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bond.jrj.com.cn/list/xfzq.shtml'
            },
            {
                'ch': {
                    'name': '债券频道-债市观察',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bond.jrj.com.cn/list/zsgc' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bond.jrj.com.cn/list/zsgc.shtml'
            },
            {
                'ch': {
                    'name': '债券频道-机构论市',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bond.jrj.com.cn/list/jgls' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bond.jrj.com.cn/list/jgls.shtml'
            },
            {
                'ch': {
                    'name': '债券频道-债基动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bond.jrj.com.cn/list/zjdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bond.jrj.com.cn/list/zjdt.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-内盘播报',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/npbb' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/npbb.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-外盘评述',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/wpps' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/wpps.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-机构报告',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/jgbg' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/jgbg.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-综合资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/zhzx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/zhzx.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-专家观点',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/mrmy' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/mrmy.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-行业新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/hyxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/hyxw.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-经济数据',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/jjsj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/jjsj.shtml'
            },
            {
                'ch': {
                    'name': '期指频道-滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/gzqh/list' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/gzqh/list.shtml'
            },
            {
                'ch': {
                    'name': '期指频道-股指期货动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/gzqh/list/gzqhdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/gzqh/list/gzqhdt.shtml'
            },
            {
                'ch': {
                    'name': '期指频道-大盘综述',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/gzqh/list/dpzs' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/gzqh/list/dpzs.shtml'
            },
            {
                'ch': {
                    'name': '国债期货频道-滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/gzfutures/list/news' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/gzfutures/list/news.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-能源化工资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/nyhgzx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/nyhgzx.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-农产品资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/ncpzx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/ncpzx.shtml'
            },
            {
                'ch': {
                    'name': '期货频道-金属资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://futures.jrj.com.cn/list/jszx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://futures.jrj.com.cn/list/jszx.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-汇市动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/hsdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/hsdt.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-经济数据',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/jjsj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/jjsj.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-汇市研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/hsyj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/hsyj.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-专家分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/zjfx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/zjfx.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-金融商品',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/nyhj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/nyhj.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-关联市场',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/glsc' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/glsc.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-人民币动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/rmbdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/rmbdt.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-央行动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/yhdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/yhdt.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-环球财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/hqcj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/hqcj.shtml'
            },
            {
                'ch': {
                    'name': '外汇频道-外汇理财',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://forex.jrj.com.cn/list/whlc' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://forex.jrj.com.cn/list/whlc.shtml'
            },
            {
                'ch': {
                    'name': '房产-房地产动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://house.jrj.com.cn/list/fdcdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://house.jrj.com.cn/list/fdcdt.shtml'
            },
            {
                'ch': {
                    'name': '房产-企业新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://house.jrj.com.cn/list/qyxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://house.jrj.com.cn/list/qyxw.shtml'
            },
            {
                'ch': {
                    'name': '财经频道-国内财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://finance.jrj.com.cn/list/guoneicj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://finance.jrj.com.cn/list/guoneicj.shtml'
            },
            {
                'ch': {
                    'name': '财经频道-财经人物',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://finance.jrj.com.cn/people' + (
                    ('rool-' + str(pg) + '.shtml') if pg >= 2 else '/'),
                'ref': 'http://finance.jrj.com.cn/people/'
            },
            {
                'ch': {
                    'name': '财经频道-商业资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://biz.jrj.com.cn/biz_index' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://biz.jrj.com.cn/biz_index.shtml'
            },
            {
                'ch': {
                    'name': '评论频道-经济时评',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://opinion.jrj.com.cn/list/jjsp' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://opinion.jrj.com.cn/list/jjsp.shtml'
            },
            {
                'ch': {
                    'name': '股票频道-亚太股市',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://stock.jrj.com.cn/list/ytgs' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://stock.jrj.com.cn/list/ytgs.shtml'
            },
            {
                'ch': {
                    'name': '财经频道-国际财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://finance.jrj.com.cn/list/guojicj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://finance.jrj.com.cn/list/guojicj.shtml'
            },
            {
                'ch': {
                    'name': '港股频道-全球市场',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://hk.jrj.com.cn/list/qqsc' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://hk.jrj.com.cn/list/qqsc.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-银行行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/hydt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/hydt.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-中资银行',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/zzyh' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/zzyh.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-外资银行',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/wzyh' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/wzyh.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-银行监管动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/jgdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/jgdt.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-观点评论',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/plyj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/plyj.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-银行卡',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/yhk' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/yhk.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-电子银行',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/dzyh' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/dzyh.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-银行家',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/yhj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/yhj.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-理财资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/yhxp' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/yhxp.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-理财诊所',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/lczs' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/lczs.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-个人信贷',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/grxd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/grxd.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-银行股评',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/yygp' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/yygp.shtml'
            },
            {
                'ch': {
                    'name': '银行频道-上市杂谈',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://bank.jrj.com.cn/list/yygsszt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://bank.jrj.com.cn/list/yygsszt.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/hyzx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/hyzx.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-保险资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/gdxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/gdxw.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-监督动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/jgdt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/jgdt.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-行业数据',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/hysj' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/hysj.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-人事变动',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/rsbd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/rsbd.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-公司新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/gsxw' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/gsxw.shtml'
            },
            {
                'ch': {
                    'name': '保险频道-高管对话',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://insurance.jrj.com.cn/list/bxmdm' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://insurance.jrj.com.cn/list/bxmdm.shtml'
            },
            {
                'ch': {
                    'name': '信托频道-行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://trust.jrj.com.cn/list/hydt' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://trust.jrj.com.cn/list/hydt.shtml'
            },
            {
                'ch': {
                    'name': '信托频道-信托理财',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://trust.jrj.com.cn/list/xtlc' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://trust.jrj.com.cn/list/xtlc.shtml'
            },
            {
                'ch': {
                    'name': '信托频道-评论研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://trust.jrj.com.cn/list/yjfx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://trust.jrj.com.cn/list/yjfx.shtml'
            },
            {
                'ch': {
                    'name': '信托频道-信托公告',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://trust.jrj.com.cn/list/xtgg' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://trust.jrj.com.cn/list/xtgg.shtml'
            },
            {
                'ch': {
                    'name': '信托频道-案例解读',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://trust.jrj.com.cn/list/aljd' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://trust.jrj.com.cn/list/aljd.shtml'
            },
            {
                'ch': {
                    'name': '黄金频道-市场快讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://gold.jrj.com.cn/list/sckx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://gold.jrj.com.cn/list/sckx.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-白银资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://gold.jrj.com.cn/list/byzx' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://gold.jrj.com.cn/list/byzx.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-交易策略',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://gold.jrj.com.cn/list/jycl' + (
                    ('-' + str(pg)) if pg >= 2 else '') + '.shtml',
                'ref': 'http://gold.jrj.com.cn/list/jycl.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://gold.jrj.com.cn/list/hydt.shtml',
                'ref': 'http://gold.jrj.com.cn/list/hydt.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-原油市场',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://gold.jrj.com.cn/list/yysc.shtml',
                'ref': 'http://gold.jrj.com.cn/list/yysc.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-外汇市场',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://gold.jrj.com.cn/list/whsc.shtml',
                'ref': 'http://gold.jrj.com.cn/list/whsc.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-黄金资讯',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://gold.jrj.com.cn/list/hjzx.shtml',
                'ref': 'http://gold.jrj.com.cn/list/hjzx.shtml'
            },
            {
                'ch': {
                    'name': '贵金属频道-宏观经济',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://gold.jrj.com.cn/list/hqcj.shtml',
                'ref': 'http://gold.jrj.com.cn/list/hqcj.shtml'
            },
        ]

        # url = 'http://stock.jrj.com.cn/hotstock/2017/12/11112623771727.shtml'
        # url = 'http://stock.jrj.com.cn/invest/2017/12/11150623772992.shtml'
        # url = 'http://opinion.jrj.com.cn/2017/12/07162723757105.shtml'
        # url = 'http://stock.jrj.com.cn/2016/10/19163921591934.shtml'
        # url = 'http://stock.jrj.com.cn/ipo/2017/10/18143223251015.shtml'
        # url = 'http://fund.jrj.com.cn/2017/12/25173523847958.shtml'
        # url = 'http://fund.jrj.com.cn/2017/12/26100423850685.shtml'
        # url = 'http://fund.jrj.com.cn/2014/04/10073817013603.shtml'
        # url = 'http://fund.jrj.com.cn/2016/12/13135621830597.shtml'
        # url = 'http://fund.jrj.com.cn/2014/04/02130216972730.shtml'
        # url = 'http://fund.jrj.com.cn/2015/10/21143119957298.shtml'
        # url = 'http://bank.jrj.com.cn/2012/05/23092213234432.shtml'
        # url = 'http://bank.jrj.com.cn/2012/04/23071812863578.shtml'
        # url = 'http://stock.jrj.com.cn/ipo/2017/09/20203823145168.shtml'
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
        ext = response.meta['ext']

        base = get_base_url(response)
        if ch['name'] == '7*24小时上市公司新闻':
            urls = re.findall(r'"infourl":"(.*?)","detail"', response.text, re.S)
        elif ch['name'] == '特殊资讯数据-机会早知道' or ch['name'] == '特色资讯数据-涨跌停揭秘':
            urls = re.findall(r'"infourl":"(.*?)","keyword"', response.text, re.S)
        elif ch['name'] == '股票频道-市况直击':
            urls = re.findall(r'http://stock.jrj.com.cn/\d+/\d+/\d+.shtml', response.text, re.S)
        elif 'news.jrj.com.cn/json' in response.url:
            urls = re.findall(r'"pcinfourl":"(.*?)","makedate"', response.text, re.S)
            iiids = re.findall(r'"iiid":(\d+),"title"', response.text, re.S)
            iiid = iiids[-1]
            infoCls = ext['infoCls']
        else:
            urls = response.xpath(
                "//div[@class='list-main']/ul/li/a/@href | //div[@class='lf2 fl']/ul/li/a/@href | //div[@class='list-s1']/ul/li/a/@href | //div[@class='clm']/ul/li/a/@href"
                "| //div[@class='grid-w630 grid-mr10']/ul/li/a/@href | //div[@class='blue list']/ul/li/a/@href | //ul[@class='ls3']/li/label/a/@href | //div[@class='md-0 pa-2']/ul/li/label/a/@href"
                "| //div[@class='left']/ul/li/span/a/@href | //div[@class='win2 nl ht10']/ul/li/a/@href | //div[@class='leftCon']/ul/li/label/a/@href | //div[@class='con']/ul/li/span/a/@href"
                "| //div[@class='newlist']/ul/li/span/a/@href | //div[@class='in']/ul/li/label/a/@href | //div[@class='p10']/ul/li/a/@href | //div[@class='divfl']/div[@class='modle']/p/a/@href"
                "| //div[@class='newslist']/ul/li/span/a/@href | //dl[@id='news']/dt/strong/a/@href").extract()
            iiid = response.xpath("//input[@id='lastId']/@value").extract_first()
            infoCls = response.xpath("//input[@id='infoCls']/@value").extract_first()
        for u in urls:
            u = urljoin(base, u)
            rcs.append({
                'ch': ch,
                'url': u,
                'ref': response.request.headers['Referer']
            })
        if ch['name'] == '贵金属频道-行业动态' or ch['name'] == '贵金属频道-原油市场' or ch['name'] == '贵金属频道-黄金资讯' or ch['name'] == '贵金属频道-外汇市场' or ch['name'] == '贵金属频道-宏观经济':
            nps.append({
                'ch': ch,
                'pg': pg + 1,
                'ext': {'infoCls': infoCls},
                'url': 'http://news.jrj.com.cn/json/news/getNews?sort=makedate&iiid=' + iiid + '&size=10&d=f&chanNum=108&infoCls='
                       + infoCls + '&vname=contents&field=iiid,title,pcinfourl,makedate,detail',
                'ref': response.request.headers['Referer']
            })
        else:
            nps.append({
                'ch': ch,
                'pg': pg + 1,
                'url': url,
                'ref': response.request.headers['Referer']
            })
        yield self.request_next(cps, rcs, nps)

    def parse_item(self, response):
        ch = response.meta['ch']
        cps = response.meta['cps']
        rcs = response.meta['rcs']
        nps = response.meta['nps']
        ext = response.meta['ext']
        ls = response.css(
            ".texttit_m1>*:not(.videcssm):not(div[align='center']):not(.table-text-one):not(div[style='MARGIN: 0px auto; WIDTH: 600px']):not(#itougu):not(.foucs_impor.mt30):not(.linknew):not(p:nth-last-child(2)[align='center']):not(.pnf):not(#addnextpagelinkbegin):not(.table-sone.mt30):not(p[sizset='17']):not(strong)").extract()
        if len(ls) < 1:
            ls = response.css('.textmain.tmf14.jrj-clear>*:not(.jj_more_new):not(.textimg.text-n1)').extract()
        if len(ls) < 1:
            ls = response.css("#IDNewsDtail>*:not(.contentzy):not(#divpage)").extract()
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
            title = response.css('.titmain>h1').re_first(r'<!--[\s]*?标题[^>]*?>[\s]*?<!--[^>]*?>([^<]+)<!--[^>]*?>')
            if title is None:
                title = response.css('.texttitbox>h1').re_first(
                    r'<!--[\s]*?标题[^>]*?>[\s]*?<!--[^>]*?>([^<]+)<!--[^>]*?>')
            if title is None:
                title = response.css('.texttitbox>h2').re_first(
                    r'<!--[\s]*?标题[^>]*?>[\s]*?<!--[^>]*?>([^<]+)<!--[^>]*?>')
            if title is None:
                title = response.css('.text-col>h1').re_first(r'<!--[\s]*?标题[^>]*?>[\s]*?<!--[^>]*?>([^<]+)<!--[^>]*?>')
            if title is None:
                title = response.css('.newsConTit>h1').re_first(
                    r'<!--[\s]*?标题[^>]*?>[\s]*?<!--[^>]*?>([^<]+)<!--[^>]*?>')
            item['title'] = title

            source = response.css(".inftop>.mh-title>.urladd>a::text").extract_first()
            if source is None:
                source = response.xpath("//p[@class='inftop']/span[2]/a/text()").extract_first()
            if source is None:
                source = response.xpath("//div[@class='newsource']/span[3]/a/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='newsource']/span[2]/a/text()").extract_first()
            if source is None:
                source = response.xpath("//p[@class='inftop']/span").re_first(r'来源[:|：]\s*?<!--[^>]*?>([^\s<]+)')
            if source is None:
                source = response.css(".inftop>.mh-title>span").re_first(r'来源[:|：]\s*?<!--[^>]*?>([^\s<]+)')
            if source is None:
                source = response.xpath("//div[@class='newsource']/span").re_first(r'来源[:|：]\s*?<!--[^>]*?>([^\s<]+)')
            if source is None:
                source = response.xpath("//p[@class='newsource']/span").re_first(r'来源[:|：]\s*?<!--[^>]*?>([^\s<]+)')
            item["source"] = source

            author = response.css('.inftop>span').re_first(r'作者[:|：]\s*?<!--[^>]*?>([^\s<]+)')
            if author is None:
                author = response.css('.inftop>.mh-title>span').re_first(r'作者[:|：]\s*?<!--[^>]*?>([^\\s<]+)')
            item['author'] = author

            pubtime = response.css('.inftop>span').re_first(r'(\d+-\d+-\d+\s*?\d+:\d+:\d+)')
            if pubtime is None:
                pubtime = response.xpath("//div[@class='newsource']/span/text()").re_first(r'(\d+年\d+月\d+日\s*?\d+:\d+)')
            if pubtime is None:
                pubtime = response.xpath("//p[@class='newsource']/span/text()").re_first(r'(\d+年\d+月\d+日\s*?\d+:\d+)')
            if pubtime is None:
                pubtime = response.css('.inftop>.mh-title>span').re_first(r'(\d+-\d+-\d+\s*?\d+:\d+:\d+)')
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = re.sub(r'\s+', ' ', pubtime.strip())
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日 %H:%M')
                    pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
            item['pubtime'] = pubtime

        i = response.xpath("//input[@id='curpage']/@value").extract_first()
        c = response.xpath("//input[@id='countpage']/@value").extract_first()

        if i == c or i is None or c is None:
            yield item
            ch['count'] = ch['count'] + 1

        else:
            rcs.insert(0, {
                'ch': ch,
                'url': re.sub(r'(/[0-9]+?/[0-9]+?/[0-9]+?)(-[0-9]+?|)(?=\.shtml)', r'\1-' + i, response.url,
                              flags=re.I),
                'ref': response.url,
                'ext': {'item': item}
            })

        yield self.request_next(cps, rcs, nps)
