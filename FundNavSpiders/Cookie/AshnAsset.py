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
    cookies = 'td_cookie=11049344; sdmenu_menu_zzjs_net=01000; PHPSESSID=94ed371f37b438c7a98c81c3f1e2980e; ZWEZy_auth=dd76pUyBb_Qh2GwJCNmz3OVAyV3VA784m_tTQaYcM6pjFWPjiOsmxbJ6g4oqnpAjaKvll0bXYZcGl6Kgpz4mjRUdXGpTd37hvfqwvr9Bu6z2MlbZGHBAbYxkJTpwDpsd6UfVyfUGxaqWHDtHu1j6SCH34w; ZWEZy__userid=3d2cyR0k_2JDphXv7HX4oVkKwOe5w7faoFy21FqRtA; ZWEZy__username=fb60Uz6JaPIlo-PVaKKCIVAG4_7XGJvhUuEpyb0pyK8; ZWEZy__groupid=87e9_vpParv0gmHKQDu68fuCDQ4A94QuwWX5Py9i; ZWEZy__nickname=0560SF-9qARGPcc2gB6zTP8aBFzK5KWELwtHB1KlSa0'

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
