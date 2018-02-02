# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class BaoyinCyInvsetSpider(GGFundNavSpider):
    name = 'FundNav_BaoyinCyInvset'
    sitename = '宝银创赢'
    channel = '投顾净值'
    allowed_domains = ['www.cymm169.com']
    start_urls = ['http://www.cymm169.com/cpjz.asp']
    username = '123456'

    def __init__(self, limit=None, *args, **kwargs):
        super(BaoyinCyInvsetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):

        yield FormRequest(url='http://www.cymm169.com/?do=ChkLogin',
                          formdata={'AdminPass': '123456',
                                    'Submit': '登 陆',
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):

        fps = [
            {
                'url': 'http://www.cymm169.com/cpjz.asp',
                'ref': 'http://www.cymm169.com/',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//table[@width='218']/tr[1]/td/a")
        for fund in funds:
            url = fund.xpath("./@href").extract_first()
            url = urljoin(get_base_url(response), url)
            fund_name = fund.xpath("./text()").extract_first()
            ips.append({
                'pg': {'page': 1, 'url': url},
                'url': lambda pg: pg['url'] + '&m=jz&page=' + str(pg['page']),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        rows = response.xpath("//table[@id='table9']/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[2]/text()").re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            if fund_name == '创赢9号对冲（华润·5号）':
                nav = row.xpath("./td[3]/text()").re_first(r'[0-9.]+')
                item['nav'] = float(nav) if nav is not None else None

                added_nav_2 = row.xpath("./td[4]/text()").re_first(r'[0-9.]+')
                item['added_nav_2'] = float(added_nav_2) if added_nav_2 is not None else None
            else:
                nav = row.xpath("./td[3]/text()").re_first(r'[0-9.]+')
                item['nav'] = float(nav)if nav is not None else None

                added_nav = row.xpath("./td[4]/text()").re_first(r'[0-9.]+')
                item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item
        url = response.meta['url']
        pg = response.meta['pg']
        totalPage = response.xpath("//a[text()='尾页']/@href").re_first(r'page=(\d+)&')
        if pg['page'] < int(totalPage):
            pg['page'] += 1
            ips.insert(0, {
                'pg': pg,
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })
        yield self.request_next(fps, ips)
