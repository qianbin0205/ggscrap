# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ZhejiangBkxtzSpider(GGFundNavSpider):
    name = 'FundNav_ZhejiangBkxtz'
    sitename = '浙江巴克夏投资'
    channel = '投资顾问'
    allowed_domains = ['www.bkxtz.com']
    start_urls = ['http://www.bkxtz.com/cn/index.htm']

    def __init__(self, limit=None, *args, **kwargs):
        super(ZhejiangBkxtzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://www.bkxtz.com/ajax_asp/newsdll_list.asp?menuid=35&page=' + str(pg) + '&sortid=0',
                'ref': 'http://www.bkxtz.com/cn/index.htm',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//ul[@class='pp_n_list']/li/a[contains(text(), '净值表现')]/@href").extract()
        for u in urls:
            u = urljoin(get_base_url(response), u)
            ips.append({
                'url': u,
                'ref': response.url,
            })

        pg = response.meta['pg']
        url = response.meta['url']
        totalpage = response.xpath("//a[@title='最后一页']/@href").re_first(r'page=(\d+)')
        if totalpage is not None:
            if pg < int(totalpage):
                fps.append({
                    'pg': pg + 1,
                    'url': url,
                    'ref': response.url,
                })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath("//div[@class='pr_title']/strong/text()").re_first(r'巴克夏月月利\S+私募基金')
        rows = response.css('div.remark>table>tbody>tr:not(:first-child)')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('td:nth-child(5)').re_first(r'\d+-\d+-\d+')
            if statistic_date == '2061-02-18':
                statistic_date = '2016-02-18'
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.css('td:nth-child(3)>p>span').re_first(r'>\s*?([0-9.]+)\s*?<')
            item['nav'] = float(nav) if nav is not None else None

            added_nav_2 = row.css('td:nth-child(4)>p>span').re_first(r'>\s*?([0-9.]+)\s*?<')
            item['added_nav_2'] = float(added_nav_2) if added_nav_2 is not None else None
            yield item

        yield self.request_next(fps, ips)


