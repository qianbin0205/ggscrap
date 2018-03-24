# coding:utf-8

from datetime import datetime
from urllib.parse import urljoin
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem
from scrapy.selector import Selector


class BinLiInvestSpider(GGFundNavSpider):
    name = 'FundNav_BinLiInvest'
    sitename = '滨利投资'
    channel = '投顾净值'
    allowed_domains = ['http://www.95binli.com']

    def __init__(self, limit=None, *args, **kwargs):
        super(BinLiInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {'url': 'http://www.95binli.com/products.asp'}
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        urls = response.xpath('//div[@class = "con2"]//a//@href').extract()
        for url in urls:
            ips_url = urljoin('http://www.95binli.com/', url)
            self.ips.append({
                'url': ips_url,
                'ref': response.url
            })

        yield self.request_next()

    def parse_item(self, response):
        funds = response.xpath('//table[@class = "table6"]//tr[position()>1]').extract()
        fund_name = Selector(response).xpath('//table[@class = "table7"]/tr//td[@colspan = "3"]/text()').extract_first()
        for fund in funds:
            nav = Selector(text=fund).xpath('//td[2]/text()').extract_first()
            added_nav = Selector(text=fund).xpath('//td[3]/text()').extract_first()
            statistic_date = Selector(text=fund).xpath('//td[1]/text()').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item

        next_href = response.xpath(
            '//div[@style = "width:100%;height:30px;line-height:30px;text-align:center;"]//a[contains(text(),"下一页")]//@href').extract_first()
        if next_href:
            ips_url = urljoin('http://www.95binli.com/products_view.asp', next_href)
            self.ips.append({
                'url': ips_url,
                'ref': response.url
            })

        yield self.request_next()
