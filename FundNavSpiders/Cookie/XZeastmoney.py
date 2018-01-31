# -*- coding: utf-8 -*-

import config
import re
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from pyquery import PyQuery


class XZeastmoneySpider(GGFundNavSpider):
    name = 'FundNav_XZeastmoney'
    sitename = '东方财富证券'
    channel = '券商资管净值'
    allowed_domains = ['www.xzsec.com']
    start_urls = ['http://www.xzsec.com/home.html']

    proxy = config.proxy
    username = '13916427906'
    cookies = 'td_cookie=11049092; td_cookie=11049087; acw_tc=AQAAACFPl2AJSAsA9bNuy/GJbNvRZs/W; xzsec_csrf_cookie_name=67702ee10e9a02b4fb74d0102103da60; tx_xzsec=9b1306b0ae9ba7b20619bba51d0d9ab49c6ea980; st_pvi=20142715828353; st_si=18433687218519; Hm_lvt_37b5100b075a06b0fd519eed8d2f561d=1517274351; userPhone=vaf4%2BseRc4j6Qe6F40DMcQ%3D%3D; Hm_lpvt_37b5100b075a06b0fd519eed8d2f561d=1517274851'

    def __init__(self, limit=None, *args, **kwargs):
        super(XZeastmoneySpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.xzsec.com/product/simu.html',
                'ref': None,
            },
            {
                'url': 'http://www.xzsec.com/product/zcgl.html',
                'ref': None
            }
        ]
        # fund_name = '同心1308湖北磁湖'
        # fund_id = 251
        # ips = [
        #     {
        #         'pg': {'page': 1, 'fund_id': fund_id},
        #         'url': lambda pg: 'http://www.xzsec.com/product/getAjaxJhjzData.html?id=' + str(pg['fund_id']) +
        #                           '&page=' + str(pg['page']),
        #         'ref': None,
        #         'ext': {'fund_name': fund_name}
        #     }
        # ]
        # yield self.request_next([], ips)

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        if response.url == 'http://www.xzsec.com/product/zcgl.html':
            funds = response.xpath("//div[@class='data-list-b tab-content']/table/tbody/tr/td[2]")
            for fund in funds:
                fund_name = fund.xpath("./a/text()").re_first(r'\S+')
                fund_id = fund.xpath("./a/@href").extract_first().split('=', 1)[1]
                ips.append({
                    'pg': {'page': 1, 'fund_id': fund_id},
                    'url': lambda pg: 'http://www.xzsec.com/product/getAjaxJhjzData.html?id=' + str(pg['fund_id']) +
                                      '&page=' + str(pg['page']),
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })

            url = response.xpath("//a[@aria-label='Next']/@href").extract_first()
            if url is not None:
                url = urljoin(get_base_url(response), url)
                fps.append({
                    'url': url,
                    'ref': response.url
                })
        else:
            funds = response.xpath("//div[@class='data-list-b tab-content'][2]/table/tbody/tr/td[2]")
            for fund in funds:
                fund_name = fund.xpath("./a/text()").re_first(r'\S+')
                fund_id = fund.xpath("./a/@href").extract_first().split('=', 1)[1]
                ips.append({
                    'pg': {'page': 1, 'fund_id': fund_id},
                    'url': lambda pg: 'http://www.xzsec.com/product/getAjaxSmjzData.html?id=' + str(pg['fund_id']) +
                                      '&page=' + str(pg['page']),
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })

            url = response.xpath("//a[@aria-label='Next']/@href").extract_first()
            if url is not None:
                url = urljoin(get_base_url(response), url)
                fps.append({
                    'url': url,
                    'ref': response.url
                })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        data = json.loads(response.text)['data']
        doc = PyQuery(data)
        if 'http://www.xzsec.com/product/getAjaxJhjzData.html' in response.url:
            for tr in doc.items('tr:not(:first-child)'):
                if '-' in tr('td').children().eq(0).text():
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    item['fund_name'] = fund_name

                    statistic_date = tr('td').children().eq(0).text()
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                    nav = tr('td').children().eq(1).text()
                    item['nav'] = float(nav) if nav is not None else None

                    added_nav = tr('td').children().eq(2).text()
                    item['added_nav'] = float(added_nav) if added_nav is not None else None
                    yield item

                elif '-' in tr('td').children().eq(1).text():
                        item = GGFundNavItem()
                        item['sitename'] = self.sitename
                        item['channel'] = self.channel
                        item['url'] = response.url

                        item['fund_name'] = tr('td').children().eq(0).text()
                        if item['fund_name'] == '' or item['fund_name'] is None:
                            item['fund_name'] = fund_name

                        statistic_date = tr('td').children().eq(1).text()
                        item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                        nav = tr('td').children().eq(2).text()
                        item['nav'] = float(nav) if nav is not None else None

                        added_nav = tr('td').children().eq(3).text()
                        item['added_nav'] = float(added_nav) if added_nav is not None else None
                        yield item
        else:
            for tr in doc.items('tr:not(:first-child)'):
                if '-' in tr('td').children().eq(0).text():
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    item['fund_name'] = fund_name

                    statistic_date = tr('td').children().eq(0).text()
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                    nav = tr('td').children().eq(2).text()
                    item['nav'] = float(nav) if nav is not None else None

                    added_nav = tr('td').children().eq(3).text()
                    item['added_nav'] = float(added_nav) if added_nav is not None else None
                    yield item

        pg = response.meta['pg']
        url = response.meta['url']
        totalPage = re.search(r'\d+\s*\/\s*(\d+)', data)
        totalPage = totalPage.group(0).split('/', 1)[1]if totalPage is not None else None
        if totalPage is not None:
            if pg['page'] < int(totalPage):
                pg['page'] += 1
                ips.insert(0, {
                    'pg': pg,
                    'url': url,
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })
        yield self.request_next(fps, ips)
