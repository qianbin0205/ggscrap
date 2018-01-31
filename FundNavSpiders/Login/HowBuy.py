# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class HowBuyInvsetSpider(GGFundNavSpider):
    name = 'FundNav_HowBuy'
    sitename = '好买'
    channel = '第三方净值'
    allowed_domains = ['howbuy.com', ]

    start_urls = []
    fps = [
        {
            'pg': 1,
            'url': 'https://simu.howbuy.com/board.htm',
            'form': {'orderType': 'Desc', 'sortField': 'jzrq', 'ejfl': '', 'gzkxd': '1', 'skey': '',
                     'page': lambda pg: str(pg), 'perPage': '100', 'allPage': '383', 'targetPage': ''},
            'ref': 'https://simu.howbuy.com/board.htm',
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(HowBuyInvsetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='https://i.howbuy.com/login/login.htm',
                          formdata={'targetUrl': '',
                                    'userName': '13916427906',
                                    'password': 'ZYYXSM123',
                                    'cookie': '30*24*60*60',
                                    'loginNameValue': '13916427906',
                                    'loginPasswd': 'yadan0319',
                                    'regFormbox': ''
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.css(r'table#spreadDetails>tr>td:first-child>input::attr(url)').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url + 'lsjz',
                'ref': url
            })
        pg = response.meta['pg']
        form = response.meta['form']
        url = response.meta['url']
        allPage = form['allPage']
        if pg < int(allPage):
            fps.append({
                'pg': pg+1,
                'url': url,
                'form': form,
                'ref': response.request.headers['Referer']
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        fund_name = response.xpath("//div[@class='trade_fund_title clearfix']/h1/text()").extract_first()
        rows = response.xpath("//div[@class='fund_data']/table/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[1]/text()").re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath("./td[2]").re_first(r'>\s*([0-9.]+)\s*<')
            item['nav'] = float(nav) if nav else None

            added_nav = row.xpath("./td[3]").re_first(r'>\s*([0-9.]+)\s*<')
            item['added_nav'] = float(added_nav) if added_nav else None

            yield item

        yield self.request_next(fps, ips)
