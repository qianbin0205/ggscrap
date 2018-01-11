# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import json


class QhhuabinSpider(GGFundNavSpider):
    name = 'FundNav_Qhhuabin'
    sitename = '前海华杉投资'
    channel = '投顾净值'
    allowed_domains = ['www.qhhscapital.com', 'simuwang.com']
    start_urls = ['http://www.qhhscapital.com/']

    def __init__(self, limit=None, *args, **kwargs):
        super(QhhuabinSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.qhhscapital.com/index.asp',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//tbody/tr/td[1]/p/span/a")

        for fund in funds:
            fund_name = fund.css('::text').extract_first()
            fund_id = fund.css('::attr(href)').re_first(r'product/(\S+).html')
            u = fund.css('::attr(href)').extract_first()
            u = urljoin(get_base_url(response), u)
            ips.append({
                'pg': 1,
                'url': 'http://dc.simuwang.com/fund/getNavList.html',
                'form': {'id': fund_id, 'muid': '55709', 'page': lambda pg: str(pg)},
                'ref': u,
                'ext': {'fund_name': fund_name},
                'username': '18637946652',
                'password': '870301'
            })

        yield FormRequest(url='http://passport.simuwang.com/index.php?m=Passport&c=auth&a=login&&rz_cback=jQuery111307024328885162334_1515675031386&type=login&name=18637946652&pass=870301&reme=1&rn=1',
                          meta={'fps': fps, 'ips': ips},
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = response.meta['pg']
        ext = response.meta['ext']
        url = response.meta['url']
        fund_name = ext['fund_name']

        datas = json.loads(response.text)['data']
        for data in datas:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = fund_name

            statistic_date = data['d']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = data['n']
            item['nav'] = float(nav)

            added_nav = data['cn']
            item['added_nav'] = float(added_nav)
            yield item

        form = response.meta['form']
        pagecount = json.loads(response.text)['pager']['pagecount']
        if pg < pagecount:
            ips.insert(0, {
                'pg': pg + 1,
                'url': url,
                'form': form,
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
