# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SiticSpider(GGFundNavSpider):
    name = 'FundNav_Sitic'
    sitename = '山东信托'
    channel = '信托净值'
    allowed_domains = ['www.sitic.com.cn']
    start_urls = ['http://www.sitic.com.cn/plus/list.php?tid=74']

    custom_settings = {
        'DOWNLOAD_DELAY': 5,
    }

    username = 'benyi'
    password = '123benyi'
    cookies = 'td_cookie=11049231; td_cookie=11049229; targetEncodinghttp://183100187=2; PHPSESSID=jhe6h7fci0eue7o7stb92m0gg2; DedeUserID=92; DedeUserID__ckMd5=ec602f707aa12cba; DedeLoginTime=1514352366; DedeLoginTime__ckMd5=9c4ef7f6177007b4'

    def __init__(self, limit=None, *args, **kwargs):
        super(SiticSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.sitic.com.cn/plus/list.php?tid=74',
                'ref': 'http://www.sitic.com.cn/member/index.php'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css(r'#content .newList ul.selling-list>li .p_title a')
        for fund in funds:
            fund_name = fund.xpath('self::a/text()').extract_first()
            url = fund.xpath('self::a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        url = response.css('#page>ul>li>a').xpath('self::a[re:test(text(), "\s*下一页\s*")]/@href').extract_first()
        if url is not None:
            url = urljoin(get_base_url(response), url)
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

        rows = response.css(r'#content .newList ul.selling-list>li')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('.p_deta::text').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row.css('.p_at::text').extract_first())

            added_nav = row.css('.p_state::text').extract_first()
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

        url = response.css('#page td a').xpath('self::a[re:test(text(), "\s*下一页\s*")]/@href').extract_first()
        if url is not None:
            url = urljoin(get_base_url(response), url)
            ips.insert(0, {
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
