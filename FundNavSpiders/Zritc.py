# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ZritcSpider(GGFundNavSpider):
    name = 'FundNav_Zritc'
    sitename = '中融信托'
    channel = '信托净值'
    allowed_domains = ['www.zritc.com']

    start_urls = []
    fps = [
        {
            'url': 'http://www.zritc.com/zrcf/ygsmjz.jsp',
            'ref': None,
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(ZritcSpider, self).__init__(limit, *args, **kwargs)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('.container .mod-10 tbody tr')
        for fund in funds:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund.css('td:nth-child(1)::text').extract_first()

            statistic_date = fund.css('td:nth-child(4)::text').extract_first()
            statistic_date = statistic_date.strip()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = fund.css('td:nth-child(2)::text').extract_first()
            item['nav'] = float(nav) if nav else nav

            added_nav = fund.css('td:nth-child(3)::text').extract_first()
            item['added_nav'] = float(added_nav) if added_nav else added_nav
            yield item

        pg = int(response.css('script::text').re_first(r'var\s+currentPage\s+=\s+(\d+);'))
        ct = int(response.css('script::text').re_first(r'var\s+countPage\s+=\s+(\d+)'))
        pg += 1
        if pg < ct:
            fps.append({
                'url': 'http://www.zritc.com/zrcf/ygsmjz.jsp',
                'headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'},
                'form': {'cpmc': '', 'searchtype': 'null', 'currpage': str(pg+1)},
                'ref': 'http://www.zritc.com/zrcf/ygsmjz.jsp'
            })

        yield self.request_next()
