# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class GuoKaiStockSpider(GGFundNavSpider):
    name = 'GuoKai_StockFundNav'
    sitename = '国开证券资管'
    channel = '发行机构'
    allowed_domains = ['www.gkzq.com.cn']
    start_urls = ['http://www.gkzq.com.cn']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'JSESSIONID=_B9JdpOdmXwnycH7rKp-aKmd5PwVWEA2eFPhji5hJyEEoUctOluY!-229239174; ecsn-session=10019762'

    def __init__(self, limit=None, *args, **kwargs):
        super(GuoKaiStockSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.gkzq.com.cn/gkzq/zqyj/zqyjInfoList11.jsp?classid=0001000100040008',
                'ref': 'http://www.gkzq.com.cn'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath('//*[@id="rewin_list_10"]/a')
        for fund in funds:
            url = fund.xpath('@href').extract_first()
            url = urljoin(get_base_url(response), url)
            print(fund)
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'type': 1}
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        exp = response.meta['ext']
        type = exp['type']
        if type == 1:
            code = response.xpath('//*[@id="list"]/div/div[2]/div[2]/div[1]/div/table/tbody/tr[3]/td[2]/p/span[2]/text()').extract_first()
            url = 'http://www.gkzq.com.cn/gkzq/zqyj/jzgl.jsp?starttime=&endtime=&pageIndex=1&pageSize=1000&code=' + code
            ips = [{'url': url, 'ref': response.url, 'ext': {'type': 2}}]
        else:
            datas = json.loads(response.text)['result']
            for data in datas:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url

                item['fund_name'] = data['name']
                statistic_date = data['pubtime']
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['statistic_date'] = statistic_date

                nav = data['dwjz']
                nav = re.search(r'([0-9.]+)', str(nav))
                nav = nav.group(0) if nav is not None else None
                item['nav'] = float(nav) if nav is not None else None

                added_nav = data['ljjz']
                added_nav = re.search(r'([0-9.]+)', str(added_nav))
                added_nav = added_nav.group(0) if added_nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item
        yield self.request_next(fps, ips)
