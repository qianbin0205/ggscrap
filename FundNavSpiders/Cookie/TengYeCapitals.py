# -*- coding: utf-8 -*-
from datetime import datetime
import json
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class TengYeCapitalsSpider(GGFundNavSpider):
    name = 'FundNav_TengYeCapitals'
    sitename = '北京腾业资本'
    channel = '投资顾问'
    allowed_domains = ['www.tengye-capitals.com']

    username = '2361483083@qq.com'
    password = '123456'
    cookies = 'clientlanguage=zh_CN; JSESSIONID=5EC0BAB34CCE436B053670C07240A801'

    def __init__(self, *args, **kwargs):
        super(TengYeCapitalsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.fps = [{
            'url': 'http://www.tengye-capitals.com/fundInfo/info.jspx',
            'ref': 'http://www.tengye-capitals.com/shareBalance/v_list.jspx'
        }]
        yield self.request_next()

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class = "flo-l left-nav"]/a[not(@style)]/@href').extract()
        name_list = response.xpath('//div[@class = "flo-l left-nav"]/a[not(@style)]/text()').extract()
        main_url = 'http://www.tengye-capitals.com/fundInfo/ferter_info.jspx?'
        for fund_name, href in zip(name_list, href_list):
            nav_url = main_url + href.split('?')[-1] + '&pageIndex=1'
            self.ips.append({
                'url': nav_url,
                'ref': response.url,
                'pg': 1,
                'ext': {
                    'fund_name': fund_name
                }
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        pg = response.meta['pg']
        rows = json.loads(response.text)['list']
        if rows:
            for row in rows:
                statistic_date = row['cDate']
                nav = row['netValue']
                added_nav = row['totalNetValue']

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav) if added_nav else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

            old_str = 'pageIndex=' + str(pg)
            new_str = 'pageIndex=' + str(pg + 1)
            next_url = response.url.replace(old_str, new_str)
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': pg + 1,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next()
