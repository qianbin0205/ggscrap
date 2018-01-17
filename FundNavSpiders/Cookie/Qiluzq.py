# -*- coding: utf-8 -*-

from scrapy import Request
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from datetime import date


class QiluzqSpider(GGFundNavSpider):
    name = 'FundNav_Qiluzq'
    sitename = '齐鲁证券'
    channel = '券商资管净值'
    allowed_domains = ['www.ztzqzg.com']
    start_urls = ['https://www.ztzqzg.com/']

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'remember_me_user=13916427906; tip_advertising=1; Hm_lvt_b45288d4cb30f48df433f9ed8f380e90=1514890208,1516095935,1516159855; advertcookie=156; ql_uid=s%3AdtqmX4JuueZ3oM0LvYCmdvphtBEO66V3.GsKjEy%2B3yK3OvpRxplcfZDLmV4SMR3A81GtmUdW9k08; remember_me_company=13916427906; userType=p; userId=YJQUp%40eI9d9z9WyXSrpuH2; login=true; Hm_lpvt_b45288d4cb30f48df433f9ed8f380e90=1516170771'

    def __init__(self, limit=None, *args, **kwargs):
        super(QiluzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='https://www.ztzqzg.com/products/product-category/t/t/',
                      meta={'fps': [], 'ips': []},
                      cookies=self.cookies,
                      callback=self.parse_fund_pre)

    def parse_fund_pre(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//div[@class='product-series-list']/ul/li/a/@data-qurl").extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            fps.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(fps, ips)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//ul[@class='sroll-div']/li")[1:]
        for fund in funds:
            fund_name = fund.xpath('./span[@class="col-md-4"]/@data-name').extract_first()
            fund_code = fund.xpath('./span[@class="col-md-4"]/@data-fundcode').extract_first()
            fund_setupdate = fund.xpath('./span[@class="col-md-4"]/@data-setupdate').extract_first()
            ips.append({
                'pg': {'page': 1, 'fund_code': fund_code, 'fund_setupdate': fund_setupdate},
                'url': lambda pg: 'https://www.ztzqzg.com/products/findCommonByCode/' + str(pg['fund_code']) + '/cpjzlist?start='
                                  + str(pg['fund_setupdate']) + '&end=' + date.isoformat(date.today())+'&pageIndex=' + str(pg['page']),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']
        pg = response.meta['pg']
        url = response.meta['url']
        fund_name = ext['fund_name']
        totalpage = response.xpath("//a[text()='尾页']/@data-index").extract_first()
        if totalpage is not None:
            rows = response.xpath("//ul/li")
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name

                statistic_date = row.xpath('./span[2]/text()').extract_first()
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                nav = row.xpath('./span[3]').re_first(r'>\s*?([0-9.]+)\s*?<')
                item['nav'] = float(nav) if nav is not None else None

                added_nav = row.xpath('./span[4]').re_first(r'>\s*?([0-9.]+)\s*?<')
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item
            if pg['page'] < int(totalpage):
                pg['page'] += 1
                ips.insert(0, {
                    'pg': pg,
                    'url': url,
                    'ref': response.request.headers['Referer'],
                    'ext': {'fund_name': fund_name}
                })
        else:
            rows = response.css('div.scroll-cpjz-list>ul>li')
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name

                statistic_date = row.xpath('./span[2]/text()').extract_first()
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                nav = row.xpath('./span[3]/text()').extract_first()
                item['nav'] = float(nav) if nav is not None else None

                added_nav = row.xpath('./span[4]/text()').extract_first()
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item

        yield self.request_next(fps, ips)
