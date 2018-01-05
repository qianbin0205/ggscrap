# -*- coding: utf-8 -*-

import re
from datetime import datetime
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from GGScrapy.items import GGNewsItem
from GGScrapy.ggspider import GGNewsSpider
import json


class SinaFinanceNewsSpider(GGNewsSpider):
    name = 'News_SinaFinance'
    sitename = '新浪财经'
    allowed_domains = ['finance.sina.com.cn', 'rool.finance.sina.com.cn', 'feed.mix.sina.com.cn']
    start_urls = []

    def __init__(self, limit=None, *args, **kwargs):
        super(SinaFinanceNewsSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        cps = [
            {
                'ch': {
                    'name': '股价异动',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://finance.sina.com.cn/column/gujiayidong.shtml',
                'ref': 'http://finance.sina.com.cn/column/gujiayidong.shtml'
            },
            {
                'ch': {
                    'name': '证券-行情要闻',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://finance.sina.com.cn/stock/hangqing/',
                'ref': 'http://finance.sina.com.cn/stock/hangqing/'
            },
            {
                'ch': {
                    'name': '市场研究',
                    'count': 0
                },
                'pg': 1,
                'url': 'http://finance.sina.com.cn/column/marketresearch.shtml',
                'ref': 'http://finance.sina.com.cn/column/marketresearch.shtml'
            },
            {
                'ch': {
                    'name': '证券-公司研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq1/gsyj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq1/gsyj/index.shtml'
            },
            {
                'ch': {
                    'name': '证券-股市评论',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq1/gspl/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq1/gspl/index.shtml'
            },
            {
                'ch': {
                    'name': '港股-市场快讯及分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gg/sckx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gg/sckx/index.shtml'
            },
            {
                'ch': {
                    'name': '港股-香港权证资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gg/xgqzzx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gg/xgqzzx/index.shtml'
            },
            {
                'ch': {
                    'name': '港股-港股IPO',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gg/ggipo/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gg/ggipo/index.shtml'
            },
            {
                'ch': {
                    'name': '港股-公司新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gg/gsxw/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gg/gsxw/index.shtml'
            },
            {
                'ch': {
                    'name': '滚动首页-港股',
                    'count': 0
                },
                'pg': 1,
                'url': lambda
                    pg: 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=52&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=' + str(
                    pg),
                'ref': 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=52&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
            },
            {
                'ch': {
                    'name': '滚动首页-美股',
                    'count': 0
                },
                'pg': 1,
                'url': lambda
                    pg: 'http://roll.finance.sina.com.cn/s/channel.php?gupiao&ch=03#col=49&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=' + str(
                    pg),
                'ref': 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=49&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
            },
            {
                'ch': {
                    'name': '基金',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/jj4/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/jj4/index_1.shtml'
            },
            {
                'ch': {
                    'name': '基金-基金业界',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/jj4/jjyj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/jj4/jjyj/index.shtml'
            },
            {
                'ch': {
                    'name': '债券-债市市场动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq2/zsscdt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq2/zsscdt/index_1.shtml'
            },
            {
                'ch': {
                    'name': '债券-债市研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq2/zsyj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq2/zsyj/index.shtml'
            },
            {
                'ch': {
                    'name': '债券',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq2/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq2/index.shtml'
            },
            {
                'ch': {
                    'name': '期货-期市要闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/qh/qsyw/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/qh/qsyw/index.shtml'
            },
            {
                'ch': {
                    'name': '期货-评论汇总',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://finance.sina.com.cn/roll/index.d.html?lid=1001&page=' + str(pg),
                'ref': 'http://finance.sina.com.cn/roll/index.d.html?lid=1001&page=1'
            },
            {
                'ch': {
                    'name': '期货-美国农业报告',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://finance.sina.com.cn/roll/index.d.html?cid=207786&page=' + str(pg),
                'ref': 'http://finance.sina.com.cn/roll/index.d.html?cid=207786&page=1'
            },
            {
                'ch': {
                    'name': '期货-农产品资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/qh/ncpzx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/qh/ncpzx/index.shtml'
            },
            {
                'ch': {
                    'name': '期货-机构看盘-农产品',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/qh/jgkp__ncp/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/qh/jgkp__ncp/index.shtml'
            },
            {
                'ch': {
                    'name': '期货-工业品资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/qh/gypzx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/qh/gypzx/index.shtml'
            },
            {
                'ch': {
                    'name': '期货-机构看盘-工业品',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/qh/jgkp__gyp/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/qh/jgkp__gyp/index.shtml'
            },
            {
                'ch': {
                    'name': '股指期货-金融衍生品资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gzqh/gzqhzxzx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gzqh/gzqhzxzx/index.shtml'
            },
            {
                'ch': {
                    'name': '机构看盘-股指期货',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gzqh/jgkp__gzqh/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gzqh/jgkp__gzqh/index.shtml'
            },
            {
                'ch': {
                    'name': '期货-能源石化资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://finance.sina.com.cn/futuremarket/oilroll.html',
                'ref': 'http://finance.sina.com.cn/futuremarket/oilroll.html'
            },
            {
                'ch': {
                    'name': '期货-机构看盘-能源石化',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/qh/jgkp__nysh/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/qh/jgkp__nysh/index.shtml'
            },
            {
                'ch': {
                    'name': '外汇',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/index.shtml'
            },
            {
                'ch': {
                    'name': '滚动新闻',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://feed.mix.sina.com.cn/api/roll/get?pageid=384&lid=2519&k=&num=50&callback=&page='
                                  + str(pg),
                'ref': 'http://finance.sina.com.cn/roll/rollnews.shtml'
            },
            {
                'ch': {
                    'name': '外汇-数据分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/sjfx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/sjfx/index.shtml'
            },
            {
                'ch': {
                    'name': '外汇-货币分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/hbfx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/hbfx/index.shtml'
            },
            {
                'ch': {
                    'name': '外汇-机构观点',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/fxyc/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/fxyc/index.shtml'
            },
            {
                'ch': {
                    'name': '外汇-汇市信息',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/hsxx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/hsxx/index.shtml'
            },
            {
                'ch': {
                    'name': '外汇-专家观点',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/hsfx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/hsfx/index.shtml'
            },
            {
                'ch': {
                    'name': '外汇-银行观点',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/wh/jggd/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/wh/jggd/index.shtml'
            },
            {
                'ch': {
                    'name': '证券-行业研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq1/xyyj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq1/xyyj/index.shtml'
            },
            {
                'ch': {
                    'name': '国际新浪财经-国际经济',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjcj/gjjj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjcj/gjjj/index.shtml'
            },
            {
                'ch': {
                    'name': '国际新浪财经-亚洲经济',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjcj/yzjj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjcj/yzjj/index.shtml'
            },
            {
                'ch': {
                    'name': '国际新浪财经-欧洲经济',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjcj/ozjj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjcj/ozjj/index.shtml'
            },
            {
                'ch': {
                    'name': '国际新浪财经-美洲经济',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjcj/mzjj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjcj/mzjj/index.shtml'
            },
            {
                'ch': {
                    'name': '国际新浪财经-其他地区',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjcj/qtdq/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjcj/qtdq/index.shtml'
            },
            {
                'ch': {
                    'name': '银行',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/index.shtml'
            },
            {
                'ch': {
                    'name': '银行-公司动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/gsdt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/gsdt/index.shtml'
            },
            {
                'ch': {
                    'name': '银行-业务与产品',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/ywycp/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/ywycp/index.shtml'
            },
            {
                'ch': {
                    'name': '银行首页-央行法规',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/yhsy_yxfg/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/yhsy_yxfg/index.shtml'
            },
            {
                'ch': {
                    'name': '银行-金融人物',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/jrrw/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/jrrw/index.shtml'
            },
            {
                'ch': {
                    'name': '银行首页-行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/yhsy_xydt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/yhsy_xydt/index.shtml'
            },
            {
                'ch': {
                    'name': '银行首页-银行评论',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/yhsy_yhpl/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/yhsy_yhpl/index.shtml'
            },
            {
                'ch': {
                    'name': '银行-私人银行',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/yh/sryh/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/yh/sryh/index.shtml'
            },
            {
                'ch': {
                    'name': '保险',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/bx3/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/bx3/index.shtml'
            },
            {
                'ch': {
                    'name': '保险公司-公司动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/bx3/bxgs_gsdt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/bx3/bxgs_gsdt/index.shtml'
            },
            {
                'ch': {
                    'name': '保险新闻-行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/bx3/bxxw_xydt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/bx3/bxxw_xydt/index.shtml'
            },
            {
                'ch': {
                    'name': '保险-保险人物',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/bx3/bxrw/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/bx3/bxrw/index.shtml'
            },
            {
                'ch': {
                    'name': '保险公司-保监会动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/bx3/bxgs_bjhdt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/bx3/bxgs_bjhdt/index.shtml'
            },
            {
                'ch': {
                    'name': '信托',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/xt2/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/xt2/index.shtml'
            },
            {
                'ch': {
                    'name': '信托-产品动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/xt2/cpdt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/xt2/cpdt/index.shtml'
            },
            {
                'ch': {
                    'name': '信托-信托行业动态',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/xt2/xtxydt/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/xt2/xtxydt/index.shtml'
            },
            {
                'ch': {
                    'name': '信托-信托评论研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/xt2/xtplyj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/xt2/xtplyj/index.shtml'
            },
            {
                'ch': {
                    'name': '贵金属-黄金资讯',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjs/hjzx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjs/hjzx/index.shtml'
            },
            {
                'ch': {
                    'name': '贵金属-黄金分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjs/hjfx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjs/hjfx/index.shtml'
            },
            {
                'ch': {
                    'name': '贵金属-白银分析',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjs/byfx/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjs/byfx/index.shtml'
            },
            {
                'ch': {
                    'name': '贵金属',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/gjs/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/gjs/index.shtml'
            },
            {
                'ch': {
                    'name': '证券-宏观研究',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://roll.finance.sina.com.cn/finance/zq1/hgyj/index_' + str(pg) + '.shtml',
                'ref': 'http://roll.finance.sina.com.cn/finance/zq1/hgyj/index.shtml'
            },
            {
                'ch': {
                    'name': '国内财经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num=10&callback=&page='
                                  + str(pg),
                'ref': 'http://finance.sina.com.cn/china/'
            },
            {
                'ch': {
                    'name': '券商',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://feed.mix.sina.com.cn/api/roll/get?pageid=186&lid=1746&num=10&callback=&page='
                                  + str(pg),
                'ref': 'http://finance.sina.com.cn/stock/quanshang/'
            },
            {
                'ch': {
                    'name': '产经',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1693&num=10&callback=&page='
                                  + str(pg),
                'ref': 'http://finance.sina.com.cn/chanjing/'
            },
            {
                'ch': {
                    'name': '新股',
                    'count': 0
                },
                'pg': 1,
                'url': lambda pg: 'http://feed.mix.sina.com.cn/api/roll/get?pageid=205&lid=1789&num=10&callback=&page='
                                  + str(pg),
                'ref': 'http://finance.sina.com.cn/stock/newstock/'
            },

        ]
        # url = 'http://finance.sina.com.cn/world/ozjj/20151106/010023691119.shtml'
        # url = 'http://finance.sina.com.cn/stock/hkstock/warrants/2017-10-24/doc-ifymzqpq3745530.shtml'
        # url = 'http://finance.sina.com.cn/money/future/agri/2017-12-28/doc-ifyqchnr6585381.shtml'
        # url = 'http://finance.sina.com.cn/stock/hkstock/marketalerts/2017-12-28/doc-ifypyuve0259352.shtml'
        # url = 'http://finance.sina.com.cn/world/mzjj/20151029/094823617257.shtml'
        # url = 'http://finance.sina.com.cn/money/forex/hbfx/2017-12-28/doc-ifyqchnr6505642.shtml'
        # url = 'http://finance.sina.com.cn/stock/marketresearch/20130419/182815211089.shtml'
        # url = 'http://finance.sina.com.cn/trust/20151209/082823970185.shtml'
        # url = 'http://finance.sina.com.cn/money/nmetal/hjzx/2017-05-10/doc-ifyfecvz0796554.shtml'
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
        if 'feed.mix.sina.com.cn' in response.url:
            data = json.loads(response.text)['result']['data']
            urls = [i['url'] for i in data]
        else:
            urls = response.xpath(
            "//div[@class='listBlk']/ul/li/a/@href | //td[@width='476']/table/tr/td/a/@href | //div[@id='d_list']/ul/li/span[@class='c_tit']/a/@href").extract()
        base = get_base_url(response)
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

        if 'blog.sina.com.cn/u/' in response.url:
            pass
        else:
            item = GGNewsItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url'] = response.url

            title = response.css('#artibodyTitle::text').extract_first()
            if title is None:
                title = response.xpath("//div[@class='atcbox']/h1/text()").extract_first()
            if title is None:
                title = response.xpath("//div[@class='articalTitle']/h2/text()").extract_first()
            item['title'] = title

            source = response.css('.time-source>[data-sudaclick="media_name"]>a::text').extract_first()
            if source is None:
                source = response.css('.time-source>[data-sudaclick="media_name"]::text').extract_first()
            if source is None:
                source = response.css('.time-source>[data-sudaclick="content_media_p"]>a::text').extract_first()
            if source is None:
                source = response.css('.time-source::text').re_first(r'[0-9]+年[0-9]+月[0-9]+日[0-9]+:[0-9]+\s+(\S+)\s*$')
            if source is None:
                source = response.xpath("//span[@id='media_name']/a/text()").extract_first()
            if source is None:
                source = response.xpath("//span[@id='media_name']/text()").extract_first()
            item['source'] = source

            author = response.xpath("//span[@id='author_ename']/a/text()").extract_first()
            item['author'] = author

            pubtime = response.css('#pub_date::text').re_first(r'([0-9]+年[0-9]+月[0-9]+日\s*[0-9]+:[0-9]+)')
            if pubtime is None:
                pubtime = response.css('.time-source::text').re_first(r'([0-9]+年[0-9]+月[0-9]+日\s*[0-9]+:[0-9]+)')
            if pubtime is None:
                pubtime = response.xpath("//span[@class='time']/text()").extract_first()
            if pubtime is None:
                pubtime = response.xpath("//span[@class='time SG_txtc']/text()").re_first(r'\d+-\d+-\d+\s*\d+:\d+:\d+')
            if pubtime is not None:
                if '年' in pubtime:
                    pubtime = re.sub(r'\s+', '', pubtime.strip())
                    pubtime = datetime.strptime(pubtime, '%Y年%m月%d日%H:%M')
                    pubtime = pubtime.strftime('%Y-%m-%d %H:%M:%S')
            item['pubtime'] = pubtime
            ls = response.css('#artibody>blockquote+div').extract()
            if len(ls) < 1:
                ls = response.css(
                '#artibody>*:not(blockquote):not(.live-finance-banner-wrap):not([data-sudaclick]):not(.xb_new_finance_app):not(font):not(.finance_app_zqtg):not(.artical-player-wrap):not(link):not(.hqimg_related):not(tbody):not(.blkComment.otherContent_01):not(.corrTxt_01):not(.blkComment):not(.moduleSingleImg01):not(iframe)'
                ':not(#PublicRelation13):not(#PublicRelation5):not(#PublicRelation11):not(.sinaads):not(style):not(script):not(div[style]):not(.tb-ad0):not(#lcs1_w):not(#relatedNewsWrap):not(#sinaads_box):not(#bottomTools):not(#lcs_wrap):not(#most_read):not(.article-info.clearfix):not(.sv_cont_c14)').extract()
            if len(ls) < 1:
                ls = response.css(
                    '.articalContent>*:not(.shareUp):not(.live-finance-banner-wrap):not(.into_bloger):not(b), .articalContent::text').extract()
            content = ''.join(ls)
            content = re.sub(r'(<img[^<>]*?\s+?src=")([^<>"]+?)("[^<>]*?\s+?real_src=")([^<>"]+?)("[^<>]*?>)',
                             r'\1\4\3\4\5', content)
            item['content'] = content

            yield item
            ch['count'] = ch['count'] + 1

        yield self.request_next(cps, rcs, nps)
