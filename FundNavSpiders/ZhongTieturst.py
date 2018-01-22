# -*- coding: utf-8 -*-

from datetime import datetime
import re
import json
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ZhongTieturstSpider(GGFundNavSpider):
    name = 'FundNav_ZhongTieturst'
    sitename = '中铁信托'
    channel = '信托净值'
    allowed_domains = ['www.crtrust.com']
    start_urls = ['http://www.crtrust.com/front/getProductsXTZQbyPage_195401472991.jhtml']

    def __init__(self, limit=None, *args, **kwargs):
        super(ZhongTieturstSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': self.start_urls[0],
                'ref': None,
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        ips = response.meta['ips']

        # key_list = re.findall(r'"Id":(.*?),', response.text)
        fund_name_list = re.findall(r'"Wcpmc":"(.*?)"', response.text)
        fund_code_list = re.findall(r'Wcpdm":"(.*?)"', response.text)
        for fund_name, fund_code in zip(fund_name_list, fund_code_list):
            ips_url = 'http://www.crtrust.com/front/getProductNav_195402134590.jhtml'
            # form其中一个参数STARDATE，不能判断,
            # 只能拉取所有JSON
            formdata = {
                'params.w_cpdm': fund_code
            }
            ips.append({
                'url': ips_url,
                'ref': response.url,
                'form': formdata,
                'ext': {'fund_name': fund_name}
            })
            yield self.request_next([], ips)

    def parse_item(self, response):

        item = GGFundNavItem()
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        nav_data = json.loads(response.text)['list']

        if nav_data:
            for detail_nav in nav_data:
                date = detail_nav['Wjzrq']
                nav = detail_nav['Wjz']

                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(date, '%Y%m%d')
                item['nav'] = float(nav)

                yield item
