# -*- coding: utf-8 -*-


from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy.http import FormRequest


class AnXinZhengQuanSpider(GGFundNavSpider):
    name = 'FundNav_AnXinZhengQuan'
    sitename = '安信证券'
    channel = '券商资管净值'
    allowed_domains = ['mall.essence.com.cn']
    start_urls = ['https://mall.essence.com.cn/servlet/json']

    def __init__(self, limit=None, *args, **kwargs):
        super(AnXinZhengQuanSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'https://mall.essence.com.cn/servlet/json',
                'form': {
                    'funcNo': '1000050',
                    'product_shelf': '1',
                    'fina_belongs': '1',
                    'page': '1',
                    'numPerPage': '1000000',
                    'fina_type': '0'
                },
                'ref': 'https://mall.essence.com.cn/mall/views/financial/financial_index.html'
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        fund_data_all_json = eval(response.text)
        fund_data_list = fund_data_all_json['results'][0]['data']
        # print(json_data)
        for fund_info in fund_data_list:
            product_code = fund_info['product_code']
            product_abbr = fund_info['product_abbr']
            product_name = fund_info['product_name']
            ips.append({
                'url': 'https://mall.essence.com.cn/servlet/json',
                'form': {
                    'funcNo': '1000055',
                    'product_code': product_code,
                    'page': '1',
                    'fund_type': '0',
                    'numPerPage': '100000000',
                },
                'ref': response.url,
                'ext': {
                    'product_name': product_name,
                    'product_code': product_code,
                    'product_abbr': product_abbr
                }
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        nav_data_all_json = eval(response.text)
        nav_info_list = nav_data_all_json['results'][0]['data']

        for nav_info in nav_info_list:
            nav_date = datetime.strptime(nav_info['nav_date'], "%Y-%m-%d")
            nav = nav_info['nav']
            cumulative_net = nav_info['cumulative_net']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = ext['product_name']
            item['statistic_date'] = nav_date
            item['nav'] = float(nav)
            item['added_nav'] = float(cumulative_net)
            yield item

        yield self.request_next(fps, ips)
