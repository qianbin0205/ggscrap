# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class BoyiInvestSpider(GGFundNavSpider):
    name = 'FundNav_BoyiInvest'
    sitename = '博颐资产'
    channel = '投顾净值'
    allowed_domains = ['www.boyiinvest.com']
    start_urls = ['http://www.boyiinvest.com/index.asp?product.html']

    username = 'by123'
    password = 'by123456'
    cookies = 'closeclick=closeclick; td_cookie=11049065; %5Fi18n=OK; %5FS%5FRESOURCE=zh%2Dcn; %5FS%5FTEMPLATEDIR=%2Ftemplate%2Fdefault; %5FS%5FLANG%5FDIR=; %5FS%5FLANG=zh%2Dcn; ASPSESSIONIDACQACSCR=LOOPGKCBOHCDHEIFDMMFPMLM'

    def __init__(self, limit=None, *args, **kwargs):
        super(BoyiInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.boyiinvest.com/index.asp?product.html',
                'ref': 'http://www.boyiinvest.com/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css(r'.leftbox .menuTree>ul>li.parent')
        for fund in funds:
            fund_name = fund.xpath('self::*/a/text()').extract_first()
            url = urljoin(get_base_url(response),
                          fund.css('.child>a').xpath(r'self::a[re:test(text(), "\s*信托净值\s*")]/@href').extract_first())
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

        rows = response.css('.rightbox>.nei_txt>table>tbody>tr')
        for row in rows:
            statistic_date = row.css('td').re_first('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')
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
