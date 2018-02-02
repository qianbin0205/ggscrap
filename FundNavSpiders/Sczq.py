# -*- coding: utf-8 -*-

from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class SczqSpider(GGFundNavSpider):
    name = 'FundNav_Sczq'
    sitename = '首创证券'
    channel = '券商资管净值'
    allowed_domains = ['assets.sczq.com.cn']
    start_urls = [
        'http://assets.sczq.com.cn/servlet/scproduct/AssetmanagmentAction?function=ProductNav&type=1&fundcode=E99']

    def __init__(self, limit=None, *args, **kwargs):
        super(SczqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'pg': 1,
                'url': lambda pg: 'http://assets.sczq.com.cn/servlet/scproduct/AssetmanagmentAction?function=ProductNav&fundcode=E99&startdate=&enddate=&curPage='
                                  + str(pg) + '&catalogNo=&reqUrl=%2Fservlet%2Fscproduct%2FAssetmanagmentAction%3Ffunction%3DProductNav',
                'ref': 'http://assets.sczq.com.cn/servlet/scproduct/AssetmanagmentAction?function=ProductNav&type=1&fundcode=E99',
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        url = response.meta['url']

        funds = response.xpath('//table/tr')[1:-1]
        for fund in funds:
            fund_code = fund.xpath("./td/a/@href").re_first(r'fundcode=(\S+)')
            ips.append({
                'pg': {'page': 1, 'fund_code': fund_code},
                'url': lambda pg: 'http://assets.sczq.com.cn/servlet/scproduct/AssetmanagmentAction?function=ProductNav&fundcode=' + str(pg['fund_code']) + '&startdate=&enddate=&curPage='
                                  + str(pg['page']) + '&catalogNo=&reqUrl=%2Fservlet%2Fscproduct%2FAssetmanagmentAction%3Ffunction%3DProductNav',
                'ref': 'http://assets.sczq.com.cn/servlet/scproduct/AssetmanagmentAction?function=ProductNav&type=1&fundcode=' + fund_code,
            })
        pg = response.xpath("//input[@class='pagenum']/@value").extract_first()
        totalpage = response.xpath("//a[@class='gocss']/@href").re_first(r'val\(\),(\d+)')
        if int(pg) < int(totalpage):
            fps.append({
                'pg': int(pg) + 1,
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        url = response.meta['url']

        rows = response.xpath('//table/tr')[1:-1]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            fund_name = row.xpath("./td[1]/a/text()").extract_first()
            item['fund_name'] = fund_name

            statistic_date = row.xpath("./td[2]/text()").extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = row.xpath("./td[3]/text()").extract_first()
            item['nav'] = float(nav)
            added_nav = row.xpath("./td[4]/text()").extract_first()
            item['added_nav'] = float(added_nav)

            yield item
        pg = response.meta['pg']
        # page = response.xpath("//input[@class='pagenum']/@value").extract_first()
        pages = response.xpath("//a[@class='gocss']/@href").re_first(r'val\(\),(\d+)')
        if pg['page'] < int(pages):
            pg['page'] += 1
            ips.insert(0, {
                'pg': pg,
                'url': url,
                'ref': response.url,
            })

        yield self.request_next(fps, ips)
