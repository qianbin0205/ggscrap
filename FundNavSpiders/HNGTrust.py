# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class HNGTrustSpider(GGFundNavSpider):
    name = 'FundNav_HNGTrust'
    sitename = '华能信托'
    channel = '发行机构'
    allowed_domains = ['www.hngtrust.com']
    start_urls = ['http://www.hngtrust.com/Channel/22870']

    def __init__(self, limit=None, *args, **kwargs):
        super(HNGTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://www.hngtrust.com/Channel/22870'
                                  + (('?_tp_t_info=' + str(pg)) if pg >= 2 else ''),
                'ref': 'http://www.hngtrust.com/Site/hngc/CN',
            }
        ]

        # url = 'http://www.hngtrust.com/Info/2052523'
        # url = 'http://www.hngtrust.com/Info/2246192'
        # url = 'http://www.hngtrust.com/Info/2251136'
        # url = 'http://www.hngtrust.com/Info/2252057'
        # yield self.request_next([], [{'url': url, 'ref': None}])

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        url = response.meta['url']
        fps = response.meta['fps']
        ips = response.meta['ips']

        pg = response.xpath(r'//td/a[text()="下一页"]').css('::attr(href)').re_first(
            r'javascript:page\D+?t_info\D+?(\d+?)\D*?')
        if pg is not None:
            fps.append({
                'pg': int(pg),
                'url': url,
                'ref': response.url
            })

        funds = response.css('td>span.date + a').xpath(r'self::a[re:test(@href, "/Info/\d+?")]')
        for fund in funds:
            u = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
            ips.append({
                'url': u,
                'ref': response.url,
                'ext': {'fund_name': fund.css('::text').re_first(r'\s*?华能信托·\s*?(.+?)\s*?(?:净值表现){0,1}\s*?$')}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        tbs = response.css('tbody')
        for tb in tbs:
            tr = tb.css('tr:first-child')
            if tr.re_first(r'日期(?:.|\n)+?信托计划单位净值(?:.|\n)+?信托计划累计净值(?:.|\n)+累计净值年化增长率') is not None:
                for tr in tb.css('tr:not(:first-child)'):
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9/]+')
                    if statistic_date is None:
                        continue
                    statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9]+/[0-9]+/[[0-9]+')
                    if statistic_date is not None:
                        statistic_date = datetime.strptime(statistic_date, '%Y/%m/%d')
                    if statistic_date is None:
                        statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9]{4}[0-9]{1,2}/[0-9]{1,2}')
                        if statistic_date is not None:
                            statistic_date = datetime.strptime(statistic_date, '%Y%m/%d')
                    item['statistic_date'] = statistic_date

                    nav = tr.css('td:nth-child(2) *::text').re_first(r'^\s*?([0-9.]+?)\s*?$')
                    item['nav'] = float(nav)

                    added_nav = tr.css('td:nth-child(3) *::text').re_first(r'^\s*?([0-9.]+?)\s*?$')
                    item['added_nav'] = float(added_nav)

                    item['fund_name'] = ext['fund_name']
                    yield item

            elif tr.re_first(r'日期(?:.|\n)+?单位净值(?:.|\n)+?累计净值') is not None:
                for tr in tb.css('tr:not(:first-child)'):
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9/]+')
                    if statistic_date is None:
                        continue
                    statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9]+/[0-9]+/[[0-9]+')
                    if statistic_date is not None:
                        statistic_date = datetime.strptime(statistic_date, '%Y/%m/%d')
                    if statistic_date is None:
                        statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9]{4}[0-9]{1,2}/[0-9]{1,2}')
                        if statistic_date is not None:
                            statistic_date = datetime.strptime(statistic_date, '%Y%m/%d')
                    item['statistic_date'] = statistic_date

                    nav = tr.css('td:nth-child(2) *::text').re_first(r'^\s*?([0-9.]+?)\s*?$')
                    item['nav'] = float(nav)

                    added_nav = tr.css('td:nth-child(3) *::text').re_first(r'^\s*?([0-9.]+?)\s*?$')
                    item['added_nav'] = float(added_nav)

                    item['fund_name'] = ext['fund_name']
                    yield item

            elif tr.re_first(r'日期(?:.|\n)+?净值') is not None:
                for tr in tb.css('tr:not(:first-child)'):
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9/]+')
                    if statistic_date is None:
                        continue
                    statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9]+/[0-9]+/[[0-9]+')
                    if statistic_date is not None:
                        statistic_date = datetime.strptime(statistic_date, '%Y/%m/%d')
                    if statistic_date is None:
                        statistic_date = tr.css('td:nth-child(1) *::text').re_first(r'[0-9]{4}[0-9]{1,2}/[0-9]{1,2}')
                        if statistic_date is not None:
                            statistic_date = datetime.strptime(statistic_date, '%Y%m/%d')
                    item['statistic_date'] = statistic_date

                    nav = tr.css('td:nth-child(2) *::text').re_first(r'^\s*?([0-9.]+?)\s*?$')
                    item['nav'] = float(nav)

                    item['fund_name'] = ext['fund_name']
                    yield item

        yield self.request_next(fps, ips)
