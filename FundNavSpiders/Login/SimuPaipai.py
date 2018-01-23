# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SimuPaipaiSpider(GGFundNavSpider):
    name = 'FundNav_SimuPaipai'
    sitename = '私募排排'
    channel = '第三方净值'
    allowed_domains = ['simuwang.com']
    start_urls = ['http://www.simuwang.com/?utm_source=8']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def __init__(self, limit=None, *args, **kwargs):
        super(SimuPaipaiSpider, self).__init__(limit, *args, **kwargs)

    def parse(self, response):
        yield FormRequest(
            url='http://passport.simuwang.com/index.php?m=Passport&c=auth&a=login&&rz_cback=jQuery11130020065956082853775_1516063850007&type=login&name=18637946652&pass=870301&reme=1&rn=1',
            callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://dc.simuwang.com/ranking/get?page=' + str(pg) + '&condition=fund_type%3A1%2C6%2C4%2C3%2C8%2C2%3Bret%3A9%3Brating_year%3A1%3Bsort_name%3Aprofit_col2%3Bsort_asc%3Adesc%3Bkeyword%3A',
                'ref': 'http://dc.simuwang.com/',
            },
            {
                'pg': 1,
                'url': lambda pg: 'http://dc.simuwang.com/ranking/get?page=' + str(
                    pg) + '&condition=newBoard%3A4%3Bret%3A9%3Brating_year%3A1%3Bistiered%3A0%3Bcompany_type%3A1%3Bsort_name%3Aprofit_col2%3Bsort_asc%3Adesc%3Bkeyword%3A',
                'ref': 'http://dc.simuwang.com/',
            },
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = response.meta['pg']
        url = response.meta['url']
        funds = json.loads(response.text)['data']
        for fund in funds:
            fund_name = fund['fund_name']
            fund_id = fund['fund_id']
            u = 'http://dc.simuwang.com/product/' + fund_id
            ips.append({
                'pg': 1,
                'url': 'http://dc.simuwang.com/fund/getNavList.html?',
                'form': {'id': fund_id, 'muid': '55709', 'page': lambda page: str(page)},
                'ref': u,
                'ext': {'fund_name': fund_name, 'fund_id': fund_id},
                'username': '18637946652',
                'password': '870301'
            })
        pagecount = json.loads(response.text)['pager']['pagecount']
        if pg < pagecount:
            fps.append({
                'pg': pg + 1,
                'url': url,
                'ref': response.request.headers['Referer']
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = response.meta['pg']
        ext = response.meta['ext']
        url = response.meta['url']
        fund_name = ext['fund_name']
        fund_id = ext['fund_id']

        date = datetime.now()
        datas = json.loads(response.text)['data']
        for data in datas:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = fund_name
            item['fund_code'] = fund_id

            statistic_date = data['d']
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
            date = statistic_date if statistic_date < date else date
            item['statistic_date'] = statistic_date

            nav = data['n']
            nav = re.search(r'([0-9.]+)', nav)
            nav = nav.group(0)if nav is not None else None
            item['nav'] = float(nav) if nav is not None else None

            added_nav = data['cnw']
            added_nav = re.search(r'([0-9.]+)', added_nav)
            added_nav = added_nav.group(0) if added_nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item

        if date >= datetime(2017, 12, 15):
            form = response.meta['form']
            pagecount = json.loads(response.text)['pager']['pagecount']
            if pg < pagecount:
                ips.insert(0, {
                    'pg': pg + 1,
                    'url': url,
                    'form': form,
                    'ref': response.request.headers['Referer'],
                    'ext': ext
                })

        yield self.request_next(fps, ips)
