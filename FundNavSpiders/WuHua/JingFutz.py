import json
from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class JingFutzSpider(GGFundNavSpider):
    name = 'FundNav_JingFutz'
    sitename = '景富投资'
    channel = '投顾净值'
    allowed_domains = ['www.jingfund.com']
    url = 'http://www.jingfund.com/'

    def __init__(self, limit=None, *args, **kwargs):
        super(JingFutzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.jingfund.com/program/userLogin.asp',
                      method='post',
                      formdata={'action': 'Login',
                                'UserName': '13916427906',
                                'Pass': '712744'
                                },
                      headers={'Referer': 'http://www.jingfund.com/user.html'},
                      callback=self.parse_login)

    def parse_login(self, response):
        fps = [
            {
                'url': 'http://www.jingfund.com/products.html',
                'ref': None
            }
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        fundLinks = response.css('div.ListLeft>ul>li>a').xpath('@href')
        ips = []
        for link in fundLinks:
            ips.append(
                    {
                        'url': self.url+link.extract(),
                        'ref': response.url
                    }
            )
        yield self.request_next([], ips)

    def parse_item(self, response):
        navInfoList = response.css('div.ListRight_Jz>table>tr')
        i = 1
        for navInfo in navInfoList:
            info = navInfo.xpath('td/text()').extract()
            if i == 1:
                i = i+1
                continue
            fundName = info[0]
            nav = info[1]
            statistic_date = info[3]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fundName
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')

            item['nav'] = float(nav)
            item['added_nav'] = None
            yield item
        yield self.request_next()
