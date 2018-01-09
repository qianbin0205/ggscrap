# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class RishengsimuSpider(GGFundNavSpider):
    name = 'FundNav_Risheng'
    sitename = '天津日昇昌资产'
    channel = '投资顾问'
    allowed_domains = ['www.rishengsimu.com']
    start_urls = ['www.rishengsimu.com']

    def __init__(self, limit=None, *args, **kwargs):
        super(RishengsimuSpider, self).__init__(limit, *args, **kwargs)

    # def start_requests(self):
    #     yield FormRequest(url='http://www.rishengsimu.com/ajax/login_h.jsp',
    #                       formdata={'cmd': 'loginMember',
    #                                 'acct': '本易',
    #                                 'pwd': 'ZYYXSM123',
    #                                 'captcha': '',
    #                                 'autoLogin': 'false'},
    #                       callback=self.parse_login)
    #
    # def parse_login(self, response):
    #     fps = [
    #         {
    #             'url': 'http://www.rishengsimu.com/col.jsp?id=110',
    #             'ref': 'http://www.rishengsimu.com',
    #         }
    #     ]
    #     yield self.request_next(fps, [])

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.rishengsimu.com/col.jsp?id=110',
                'ref': 'http://www.rishengsimu.com',
                'username': '本易',
                'password': 'ZYYXSM123',
                'cookies': '_cliid=FyoIBcoCQbLAkCzw; loginMemberCacct=rswealth; loginMemberAcct=%E6%9C%AC%E6%98%93; _lastEnterDay=2018-01-08; _siteStatId=d4f9e912-4090-4141-bd5d-b05554f5629c; _siteStatDay=20180108; _siteStatRedirectUv=redirectUv_7599919; _siteStatVisit=visit_7599919; lastLoginTime75999198=2018-01-08; www.rishengsimu.com__VSIGN=AIjbzNIFCgQ4alQ0ELj4wbQG; _siteStatReVisit=reVisit_7599919; td_cookie=11049215; _FSESSIONID=0-yZtH-mbR852wfO; _siteStatVisitTime=1515401982634'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):

        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//td[@class='J_newsTitle newsTitle']")
        for fund in funds:
            url = urljoin(get_base_url(response), fund.xpath("./a/@href").extract_first())
            fund_name = fund.xpath("./a/text()").re_first(r'日昇昌仁\S+私募投资基金')
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = ext['fund_name']

        statistic_date = response.xpath("//tr/td/p/span/text()").re_first(r'净值日期:(\d+-\d+-\d+)')
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
        nav = response.xpath("//tr/td/p/span/text()").re_first(r'单位净值：(\S+)')
        item['nav'] = float(nav) if nav is not None else None

        added_nav = response.xpath("//tr/td/p/span/text()").re_first(r'累计净值：(\S+)')
        item['added_nav'] = float(added_nav) if added_nav is not None else None

        yield item

        yield self.request_next(fps, ips)
