import hashlib
import traceback
from datetime import datetime
from urllib.parse import quote
from scrapy import Item, Field
from scrapy import Request, FormRequest
from ggmssql.pool import Pool
from GGScrapy import GGSpider
import config


# 基金净值Spider基类
class GGFundNavSpider(GGSpider):
    custom_settings = {
        'ITEM_PIPELINES': {'FundNavSpiders.GGFundNavPipeline': 300}
    }

    dbPool = Pool(config.fund_nav['db']['host'],
                  config.fund_nav['db']['port'],
                  config.fund_nav['db']['user'],
                  config.fund_nav['db']['pswd'],
                  config.fund_nav['db']['name'],
                  timeout=config.fund_nav['db']['timeout'])

    fps = []  # fund (list) pages
    ips = []  # item (list) pages

    def __init__(self, *args, **kwargs):
        super(GGFundNavSpider, self).__init__(*args, **kwargs)

    def request_next(self, *args):
        self.fps = args[0] if args[0:] else self.fps
        self.ips = args[1] if args[1:] else self.ips

        ps = self.ips or self.fps  # pages
        pf = self.parse_item if self.ips else self.parse_fund  # parse function
        if ps:
            pi = ps.pop(0)  # page info

            ext = pi['ext'] if 'ext' in pi else {}
            pg = pi['pg'] if 'pg' in pi else None

            url = pi['url'] if 'url' in pi else None
            req_url = url(pg) if callable(url) else url

            ref = pi['ref'] if 'ref' in pi else None
            req_ref = ref(pg) if callable(ref) else ref

            headers = pi['headers'] if 'headers' in pi else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = req_ref

            form = pi['form'] if 'form' in pi else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return FormRequest(url=req_url, headers=headers, formdata=formdata, dont_filter=True, callback=pf,
                                   meta={'pi': pi,
                                         'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                         'headers': headers, 'form': form,
                                         'fps': self.fps, 'ips': self.ips})
            else:
                body = pi['body'] if 'body' in pi else None
                body = body(pg) if callable(body) else body
                method = 'POST' if body else 'GET'
                return Request(req_url, method=method, headers=headers, body=body, dont_filter=True, callback=pf,
                               meta={'pi': pi,
                                     'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                     'headers': headers, 'body': body,
                                     'fps': self.fps, 'ips': self.ips})

    def parse_fund(self, response):
        pass

    def parse_item(self, response):
        pass


# 基金净值Item
class GGFundNavItem(Item):
    hkey = Field()  # 哈希主键

    groupname = Field()  # 分组名称
    sitename = Field()  # 站点名称
    channel = Field()  # 频道名称

    url = Field()  # 链接地址
    fund_name = Field()  # 基金名称
    statistic_date = Field()  # 统计日期
    fund_code = Field()  # 基金代码
    nav = Field()  # 单位净值(单位: 元)
    added_nav = Field()  # 累计净值(单位: 元)
    nav_2 = Field()  # 含业绩报酬的单位净值(单位: 元)
    added_nav_2 = Field()  # 含业绩报酬的累计单位净值(单位: 元)
    total_nav = Field()  # 总资产净值(单位: 元)
    share = Field()  # 资产份额(单位: 份)
    income_value_per_ten_thousand = Field()  # 每万份计划收益(单位: 元)
    d7_annualized_return = Field()  # 7日年化收益率(单位: %)


# 基金净值Pipeline
class GGFundNavPipeline(object):
    def process_item(self, item, spider):
        return item
        # try:
        #     groupname = item['groupname'] if 'groupname' in item else spider.groupname
        #     groupname = groupname.strip() if isinstance(groupname, str) else None
        #     groupname = groupname if groupname != '' else None
        #     assert groupname is None or groupname != ''
        #
        #     sitename = item['sitename'] if 'sitename' in item else None
        #     sitename = sitename.strip() if isinstance(sitename, str) else None
        #     assert sitename is not None and sitename != ''
        #
        #     channel = item['channel'] if 'channel' in item else None
        #     channel = channel.strip() if isinstance(channel, str) else None
        #     assert channel is not None and channel != ''
        #
        #     url = item['url'] if 'url' in item else None
        #     url = url.decode() if isinstance(url, bytes) else url
        #     url = url.strip() if isinstance(url, str) else None
        #     assert url is not None and url != ''
        #
        #     fund_name = item['fund_name'] if 'fund_name' in item else None
        #     fund_name = fund_name.strip() if isinstance(fund_name, str) else None
        #     assert fund_name is not None and fund_name != ''
        #
        #     statistic_date = item['statistic_date'] if 'statistic_date' in item else None
        #     assert isinstance(statistic_date, datetime)
        #     statistic_date = item['statistic_date'].strftime('%Y-%m-%d')
        #
        #     fund_code = item['fund_code'] if 'fund_code' in item else None
        #     fund_code = fund_code.strip() if isinstance(fund_code, str) else None
        #     fund_code = fund_code if fund_code != '' else None
        #     assert fund_code is None or fund_code != ''
        #
        #     nav = item['nav'] if 'nav' in item else None
        #     assert nav is None or isinstance(nav, float) or isinstance(nav, int)
        #
        #     added_nav = item['added_nav'] if 'added_nav' in item else None
        #     assert added_nav is None or isinstance(added_nav, float) or isinstance(added_nav, int)
        #
        #     nav_2 = item['nav_2'] if 'nav_2' in item else None
        #     assert nav_2 is None or isinstance(nav_2, float) or isinstance(nav_2, int)
        #
        #     added_nav_2 = item['added_nav_2'] if 'added_nav_2' in item else None
        #     assert added_nav_2 is None or isinstance(added_nav_2, float) or isinstance(added_nav_2, int)
        #
        #     total_nav = item['total_nav'] if 'total_nav' in item else None
        #     assert total_nav is None or isinstance(total_nav, float) or isinstance(total_nav, int)
        #
        #     share = item['share'] if 'share' in item else None
        #     assert share is None or isinstance(share, float) or isinstance(share, int)
        #
        #     income_value_per_ten_thousand = item[
        #         'income_value_per_ten_thousand'] if 'income_value_per_ten_thousand' in item else None
        #     assert income_value_per_ten_thousand is None or isinstance(income_value_per_ten_thousand,
        #                                                                float) or isinstance(
        #         income_value_per_ten_thousand, int)
        #
        #     d7_annualized_return = item['d7_annualized_return'] if 'd7_annualized_return' in item else None
        #     assert d7_annualized_return is None or isinstance(d7_annualized_return, float) or isinstance(
        #         d7_annualized_return, int)
        #
        #     md5 = hashlib.md5()
        #     seed = 'sitename=' + quote(sitename)
        #     seed += '&channel=' + quote(channel)
        #     seed += '&fund_name=' + quote(fund_name)
        #     seed += '&statistic_date=' + quote(statistic_date)
        #     if fund_code is not None:
        #         seed += '&fund_code=' + quote(fund_code)
        #     if nav is not None:
        #         seed += '&nav=' + quote(str(nav))
        #     if added_nav is not None:
        #         seed += '&added_nav=' + quote(str(added_nav))
        #     if nav_2 is not None:
        #         seed += '&nav_2=' + quote(str(nav_2))
        #     if added_nav_2 is not None:
        #         seed += '&added_nav_2=' + quote(str(added_nav_2))
        #     if total_nav is not None:
        #         seed += '&total_nav=' + quote(str(total_nav))
        #     if share is not None:
        #         seed += '&share=' + quote(str(share))
        #     if income_value_per_ten_thousand is not None:
        #         seed += '&income_value_per_ten_thousand=' + quote(str(income_value_per_ten_thousand))
        #     if d7_annualized_return is not None:
        #         seed += '&d7_annualized_return=' + quote(str(d7_annualized_return))
        #     md5.update(seed.encode('utf-8'))
        #     hkey = md5.hexdigest()
        #     item['hkey'] = hkey
        #
        #     conn = spider.dbPool.acquire()
        #     cursor = conn.cursor()
        #     try:
        #         table = config.fund_nav['db']['table']
        #         cursor.execute(
        #             'SELECT TOP 1 hkey FROM ' + table + ' WHERE sitename=%s AND channel=%s AND fund_name=%s AND statistic_date=%s ORDER BY tmstamp',
        #             (sitename, channel, fund_name, statistic_date,))
        #         row = cursor.fetchone()
        #         if row is None:
        #             cursor.execute(
        #                 'INSERT INTO ' + table + ' (hkey,groupname,sitename,channel,url,fund_name,statistic_date,fund_code,nav,added_nav,nav_2,added_nav_2,total_nav,share,income_value_per_ten_thousand,d7_annualized_return) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        #                 (hkey, groupname, sitename, channel, url, fund_name, statistic_date, fund_code, nav, added_nav,
        #                  nav_2, added_nav_2, total_nav, share, income_value_per_ten_thousand, d7_annualized_return,))
        #         elif row['hkey'] != hkey:
        #             cursor.execute(
        #                 'UPDATE ' + table + ' SET hkey=%s,groupname=%s,url=%s,fund_code=%s,nav=%s,added_nav=%s,nav_2=%s,added_nav_2=%s,total_nav=%s,share=%s,income_value_per_ten_thousand=%s,d7_annualized_return=%s,update_time=GETDATE() WHERE hkey=%s',
        #                 (hkey, groupname, url, fund_code, nav, added_nav, nav_2, added_nav_2, total_nav, share,
        #                  income_value_per_ten_thousand, d7_annualized_return, row['hkey'],))
        #     finally:
        #         cursor.close()
        #         spider.dbPool.release(conn)
        # except:
        #     spider.crawler.engine.close_spider(spider, 'pipeline error!')
        #     spider.crawler.stats.set_value('exit_emsg', traceback.format_exc())
        #     spider.crawler.stats.set_value('exit_emsg_item', item)
        #     spider.crawler.stats.set_value('exit_code', 1)
        # finally:
        #     return item
