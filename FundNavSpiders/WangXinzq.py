# -*- coding: utf-8 -*-

import re
from datetime import datetime
from urllib.parse import urljoin
from GGScrapy.ggspider import GGFundNavSpider
from GGScrapy.items import GGFundNavItem


class WangXinzqSpider(GGFundNavSpider):
    name = 'FundNav_WangXinzq'
    sitename = '网信证券'
    channel = '券商资管净值'
    allowed_domains = ['www.wxzq.com']
    start_urls = ['http://www.wxzq.com/jzgb.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(WangXinzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.wxzq.com/jzgb.html',
                'ref': None,
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        href = response.css('ul.kUi_list a::attr(href)').extract_first()
        ips_url = urljoin('http://www.wxzq.com/', href)
        ips.append({
            'url': ips_url,
            'ref': response.url
        })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        ips = response.meta['ips']

        fund_info = response.css('div.kUi_artice').xpath('string(.)').extract_first().strip()
        # 特殊结构：http://www.wxzq.com/detail/513103.html
        # 会有1个日期对应多个产品的情况
        date = re.findall('截止(\d{0,4}年\d{0,2}月\d{0,2}日)', fund_info)[0]

        fund_name_list = re.findall('\s+(.+?)份额净值：', fund_info, re.DOTALL)
        nav_list = re.findall('净值：(\d+\.\d*)?', fund_info, re.DOTALL)

        item = GGFundNavItem()
        for fund_name, nav in zip(fund_name_list, nav_list):
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(date, '%Y年%m月%d日')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = None

            yield item

        next_href = response.xpath("//a[contains(./text(),'下一')]/@href").extract_first()
        if next_href:
            # 在第50页的时候，翻到51,52,53往后所有页数，点击会跳转至首页，
            # 所以只能通过下一页去翻页，如果没有取到下一页HREF就判断为最后一页
            ips_url = urljoin('http://www.wxzq.com/', next_href)
            ips.append({
                'url': ips_url,
                'ref': response.url
            })

            yield self.request_next([], ips)
