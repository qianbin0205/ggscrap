# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class HoldGoodAssetSpider(GGFundNavSpider):
    name = 'FundNav_HoldGoodAsset'
    sitename = '杭州厚德载富财富'
    channel = '投资顾问'
    allowed_domains = ['www.holdgood.net']
    start_urls = ['http://www.holdgood.net/index.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(HoldGoodAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.holdgood.net/FrontMembers.do?method=doLogin01&compId=FrontMembers_login01-1416478560184',
                          formdata={'membername': "285555646@qq.com",
                                    'password': "050835"
                                    },
                          callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.holdgood.net/products_list/pmcId=22.html',
                'ref': 'http://www.holdgood.net/index.html',
                'pg': {'page': 1}
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = response.xpath('//ul[@class="mainul productlist-02"]/li/div/ul/li/h1/strong/a')
        for fund in funds:
            url = fund.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            fund_name = fund.xpath('./text()').extract_first().strip()
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })
        pages = response.xpath('//div[@class="total"]').re(r'\d+')
        page = int(pages[0])
        total_page = int(pages[-1])
        if page < total_page:
            next_page = str(page + 1)
            url = 'http://www.holdgood.net/products_list/pmcId=22&pageNo_FrontProducts_list01-1416471746544=' + next_page + '&pageSize_FrontProducts_list01-1416471746544=20.html'
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
        if fund_name == '厚道魔方1号定增对冲对策略基金' or fund_name == '厚道定向增发5号私募基金':
            rows = response.xpath('//div[@class="FrontProducts_detail02-1504768440814_htmlbreak1"]/table[1]/tbody/tr')[1:]
        else:
            rows = response.xpath('//div[@class="FrontProducts_detail02-1504768440814_htmlbreak1"]/table[1]/tbody/tr')[0:]

        # 获取系统时间的年份（净值日期为月日格式时使用）
        year = datetime.now().year
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            if fund_name == '厚道源丰私募证券投资基金':
                statistic_date_str = row.xpath("./td[1]/text()").re_first(r'\d+月\d+日')
                statistic_date = str(year) + '年' + statistic_date_str
                statistic_date = datetime.strptime(statistic_date, '%Y年%m月%d日')
                if statistic_date > datetime.now():
                    statistic_date = str(year - 1) + '年' + statistic_date_str
                    statistic_date = datetime.strptime(statistic_date, '%Y年%m月%d日')
                nav = row.xpath("./td[2]/text()").re_first(r'[0-9.]+')
            else:
                statistic_date = row.xpath("./td[1]/text()").re_first(r'\d+-\d+-\d+')
                if statistic_date is None:
                    statistic_date = row.xpath("./td[1]/span/text()").re_first(r'\d+-\d+-\d+')
                if statistic_date is None:
                    statistic_date = row.xpath("./td[1]/div/text()").re_first(r'\d+-\d+-\d+')
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')

                nav = row.xpath("./td[2]/text()").re_first(r'[0-9.]+')
                if nav is None:
                    nav = row.xpath("./td[2]/span/text()").re_first(r'[0-9.]+')
                if nav is None:
                    nav = row.xpath("./td[2]/div/text()").re_first(r'[0-9.]+')

            item['statistic_date'] = statistic_date
            item['nav'] = float(nav)
            yield item

        yield self.request_next(fps, ips)
