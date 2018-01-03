# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class AshnAssetSpider(GGFundNavSpider):
    name = 'FundNav_AshnAsset'
    sitename = '上海奥索灏纳资产'
    channel = '投顾净值'
    allowed_domains = ['www.ashnasset.com.cn']
    start_urls = ['http://www.ashnasset.com.cn/index.php?m=content&c=index&a=show&catid=15&id=2']

    def __init__(self, limit=None, *args, **kwargs):
        super(AshnAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.ashnasset.com.cn/index.php?m=content&c=index&a=show&catid=15&id=2',
                'ref': 'http://www.ashnasset.com.cn/',
                'username': 'zym',
                'password': '13916427906',
                'cookies': 'PHPSESSID=e9df475bbfa5b16a3fe29be23ce527ca; ZWEZy_auth=61cdVpwZSWQ0aT5sdlydnxsTONfj549B12l-7HXKq6gxGrC1JB7UhvQcpWLLMQkV7eF1qgOZYWlP5Fgufu4PbEVY5U--zHR5JEgd6mPy5Mi5lv-fOYzm3XTmX_EaWlTTMch963UEkDGNlWv2OhdM7tb_xg; ZWEZy__userid=7add0oSQ4fQwhnyWilcEO9R6uu4ZVDYBxh-ByFQx-A; ZWEZy__username=69d2Qfag3RTfncCO-PoYkNh87Ikcv4Qp0ZQJB0KREeE; ZWEZy__groupid=9f43gxEq04-Q4I5aBE4HWF0bfb6tMqfUjNnzOzj9; ZWEZy__nickname=2a05R2BukgytvwIzkhRPtt17zEdwiDNPjmWrZbVKkbM; sdmenu_menu_zzjs_net=01000; td_cookie=11049327'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css(r'.product1>.product1l>ul>li>a')
        for fund in funds:
            fund_name = fund.xpath('self::a/text()').extract_first()
            url = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
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

        rows = response.css('#con_one_1 tbody>tr')
        for row in rows:
            statistic_date = row.css('td:first-child').re_first('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')
            if statistic_date is None:
                continue

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = ext['fund_name']

            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(row.css('td:nth-child(2)').re_first('>\s*?([0-9.]+?)\s*?<'))

            yield item

        yield self.request_next(fps, ips)
