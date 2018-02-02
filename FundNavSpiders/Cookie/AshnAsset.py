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

    username = 'zym'
    password = '13916427906'
    cookies = 'sdmenu_menu_zzjs_net=01000; PHPSESSID=ef97e52267904f13f741193c2c26f2c0; td_cookie=11049081; ZWEZy_auth=5754ACXSmsHAxaiwjytoDrfiBhqxnY_tZniaGcQ3yC14Z_m98O_o-dnrolkeUAJ4haEbyVN3ZyhfHV2oxNv7ixpCww3eR-1JO0lJz9A7loQwJOPD6lEdex3mKRuP6VdUKBWUvd0tn3RAg65TYvIGCJ-I1Q; ZWEZy__userid=8038pd5nn8OfOzN3dr3LtIYy5pqXao3G9zqJKTXC-w; ZWEZy__username=ac9ezMamC-1zrWwStzbar178h03mBtrughZScd33_-w; ZWEZy__groupid=7437jWkGp1BMjH80c1QtWqSN-OxzXWt0R92Rzxld; ZWEZy__nickname=ef78gPReNuqWznekddX2lp_0Kox7UFh72TVA8UsTyfA'

    def __init__(self, limit=None, *args, **kwargs):
        super(AshnAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.ashnasset.com.cn/index.php?m=content&c=index&a=show&catid=15&id=2',
                'ref': 'http://www.ashnasset.com.cn/'
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
