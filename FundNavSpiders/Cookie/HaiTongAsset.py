# -*- coding: utf-8 -*-

from scrapy import Request
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class HaiTongAssetSpider(GGFundNavSpider):
    name = 'FundNav_HaiTongAsset'
    sitename = '海通资产'
    channel = '投资顾问'
    allowed_domains = ['www.htsamc.com']
    start_urls = ['http://www.htsamc.com/main/products/collectfinancial/850011/productoverview.shtml']

    username = '37152619880731162X'
    password = '871203'
    cookies = 'cookiesession1=43E19F30KRJUEL2DHJRVO3DJE4J5F468; JSESSIONID=abchkZ4PrklFN4tAX6pfw; tk_stat_b=0; tk_stat_id=25B80019385B4C8B9FB1A84554D3925; tk_stat_z=none; tk_stat_c=1517469763948; tk_stat_e=83; tk_stat_a=83'

    def __init__(self, limit=None, *args, **kwargs):
        super(HaiTongAssetSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.htsamc.com/main/products/collectfinancial/index.shtml',
                      meta={'fps': [], 'ips': []},
                      cookies=self.cookies,
                      callback=self.parse_fund_pre)

    def parse_fund_pre(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        fund_tables = response.xpath('//table[@class="pro_list_tb"]/tr/td/a')[1:]
        fund_divs = response.xpath('//div[@class="revoke_btn"]/a')
        fund_tables.extend(fund_divs)
        params_set = []

        for fund in fund_tables:
            params = fund.xpath('./@onclick').re('\d+')[1:]
            if params not in params_set:
                params_set.append(params)

                fundtp1 = str(params[0])
                fundtp2 = ''
                if len(params) >= 2:
                    for param in params[1:]:
                        fundtp2 += param + ','
                    fundtp2 = fundtp2[:-1]

                url = 'http://www.htsamc.com/servlet/fund/FundAction?function=getFundInfo&cycleday=&fundid=&fundtp1=' + fundtp1 + '&fundtp2=' + fundtp2 + '&orderby=&orderline=asc&rowOfPage=1000'
                fps.append({
                    'url': url,
                    'ref': response.url
                })
        yield self.request_next(fps, ips)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        funds = response.xpath(r'//span[@class="s_black"]')
        for fund in funds:
            fund_code = fund.xpath(r'./text()').extract_first().strip()
            print(fund_code)
            ips.append({
                'url': 'http://www.htsamc.com/servlet/fund/FundAction?function=getFundNav&fundCode=' + fund_code + '&pageNumber=1&rowOfPage=10000',
                'ref': response.url
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        rows = response.xpath(r'//div[@class="fundid_data"]/table/tbody/tr')
        for row in rows:
            fund_name = row.xpath(r'./td[1]/span/text()').extract_first()
            if fund_name is None:
                continue

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            if fund_name == '现金赢家':
                statistic_date = row.xpath('./td[3]/text()').re_first(r'\d+-\d+-\d+')
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                income_value_per_ten_thousand = row.xpath('./td[4]/span/text()').re_first(r'[0-9.]+')
                d7_annualized_return = row.xpath('./td[5]/span/text()').re_first(r'[0-9.]+')

                item['statistic_date'] = statistic_date
                item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand)
                item['d7_annualized_return'] = float(d7_annualized_return)
            else:
                statistic_date = row.xpath('./td[2]/text()').re_first(r'\d+-\d+-\d+')
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                nav = row.xpath('./td[3]/span/text()').re_first(r'[0-9.]+')
                added_nav = row.xpath('./td[4]/span/text()').re_first(r'[0-9.]+')

                item['statistic_date'] = statistic_date
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
            yield item

        yield self.request_next(fps, ips)
