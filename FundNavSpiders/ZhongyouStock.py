# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhongyouStockSpider(GGFundNavSpider):
    name = 'FundNav_zystock'
    sitename = '中邮证券'
    channel = '券商资管净值'
    allowed_domains = ['www.cnpsec.com.cn']
    start_urls = ['http://www.cnpsec.com.cn']

    def __init__(self, *args, **kwargs):
        super(ZhongyouStockSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.cnpsec.com.cn/web/list.htm?menuId=08&subId=0801&classId=080106',
                'ref': 'http://www.cnpsec.com.cn/web/list.htm?menuId=08&subId=0801&classId=080104&menuId=08&subId=0805&classId=0805',
                'ext': {'pg': 1, 'type': 0}

            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = int(response.meta['ext']['pg'])
        type = int(response.meta['ext']['type'])
        if type == 0:
            fps.append({
                'url': 'http://www.cnpsec.com.cn/web/list.ashx',
                'form': {'classid': '080106',
                         'pageIndex': str(pg),
                         'infoFlag': 'finfo',
                         'type': '1',
                         'datalen': '20',
                         'hrefURL': 'L2N0enEvenh6eC96eDAzLmh0bWw/bWVudUlkPTA4JnN1YklkPTA4MDEmY2xhc3NJZD0wODAxMDY=',
                         'jsontype': 'json_4'},
                'ref': response.url,
                'ext': {'pg': str(pg + 1), 'type': '1'}
            })
        else:
            datas = json.loads(response.text)['result']
            totalPages = int(json.loads(response.text)['totalPages'])
            if totalPages > pg:
                fps.append({
                    'url': 'http://www.cnpsec.com.cn/web/list.ashx',
                    'form': {'classid': '080106',
                             'pageIndex': str(pg),
                             'infoFlag': 'finfo',
                             'type': '1',
                             'datalen': '20',
                             'hrefURL': 'L2N0enEvenh6eC96eDAzLmh0bWw/bWVudUlkPTA4JnN1YklkPTA4MDEmY2xhc3NJZD0wODAxMDY=',
                             'jsontype': 'json_4'},
                    'ref': response.url,
                    'ext': {'pg': str(pg + 1), 'type': '1'}
                })
            for data in datas:
                url = 'http://www.cnpsec.com.cn/web/GetInfo.ashx?classId=080106&filter=guid&fv=' + str(
                    data['infoid']) + '&datalen=title&hrefURL=&jsontype=json_4'
                ips.append({
                    'url': url,
                    'ref': response.url
                })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        datas = json.loads(response.text)['result']
        for data in datas:
            contents = data['content']
            regex_start1 = re.compile('<TD class=.{1,7}>.{1,30}</TD>')
            regex_start2 = re.compile('<FONT size=2 face=宋体>.{1,30}</FONT>')

            table1 = regex_start1.findall(contents)
            table2 = regex_start2.findall(contents)
            index = 3
            item = GGFundNavItem()
            for td in table1:
                n = index % 3
                if n == 0:
                    item = GGFundNavItem()
                    fund_name = data['title']
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = re.sub(r'净值\s*$', '', fund_name)
                if n == 0:
                    statistic_date = self.parse_time(td)
                    if statistic_date is None:
                        continue
                    item['statistic_date'] = statistic_date
                    index = index + 1
                if n == 1:
                    nav = re.search('\d{1,2}\.\d{1,6}', td, flags=0).group()
                    nav = re.search(r'([0-9.]+)', str(nav))
                    nav = nav.group(0) if nav is not None else None
                    item['nav'] = float(nav) if nav is not None else None
                    index = index + 1
                if n == 2:
                    added_nav = re.search('\d{1,2}\.\d{1,6}', td, flags=0).group()
                    added_nav = re.search(r'([0-9.]+)', str(added_nav))
                    added_nav = added_nav.group(0) if added_nav is not None else None
                    item['added_nav'] = float(added_nav) if added_nav is not None else None
                    index = index + 1
                    yield item
            index = 3
            item = GGFundNavItem()
            for td in table2:
                n = index % 3
                index = index + 1
                if n == 0:
                    item = GGFundNavItem()
                    fund_name = data['title']
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                if n == 0:
                    statistic_date = self.parse_time(td)
                    if statistic_date is None:
                        continue
                    item['statistic_date'] = statistic_date
                    index = index + 1
                if n == 1:
                    nav = re.search('\d{1,2}\.\d{1,6}', td, flags=0).group()
                    nav = re.search(r'([0-9.]+)', str(nav))
                    nav = nav.group(0) if nav is not None else None
                    item['nav'] = float(nav) if nav is not None else None
                    index = index + 1
                if n == 2:
                    added_nav = re.search('\d{1,2}\.\d{1,6}', td, flags=0).group()
                    added_nav = re.search(r'([0-9.]+)', str(added_nav))
                    added_nav = added_nav.group(0) if added_nav is not None else None
                    item['added_nav'] = float(added_nav) if added_nav is not None else None
                    index = index + 1
                    yield item
        yield self.request_next(fps, ips)

    # 日期处理2017年05月26日----2018/1/15------2015-12-18
    def parse_time(self, td):
        index = td.find("年")
        flg = 1
        if index > 0:
            statistic_date = re.search('\d{4}年\d{1,2}月\d{1,2}日', td, flags=0)
        index = td.find('-')
        if index > 0:
            statistic_date = re.search('\d{4}-\d{1,2}-\d{1,2}', td, flags=0)
            flg = 2
        else:
            statistic_date = re.search('\d{4}\/\d{1,2}\/\d{1,2}', td, flags=0)
            flg = 3
        if statistic_date is None:
            return None
        statistic_date = statistic_date.group()
        if flg == 1:
            statistic_date = datetime.strptime(statistic_date, '%Y年%m月%d日')
        if flg == 2:
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
        if flg == 3:
            statistic_date = datetime.strptime(statistic_date, '%Y/%m/%d')
        return statistic_date
