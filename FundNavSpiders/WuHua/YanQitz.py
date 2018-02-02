import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy import FormRequest
# import requests


class YanQitzSpider(GGFundNavSpider):
    name = 'FundNav_YanQitz'
    sitename = '言起投资'
    channel = '投顾净值'
    allowed_domains = ['www.yanqicapital.com']
    start_urls = ['http://www.yanqicapital.com/Show_html/aspx/PorductsDetails.aspx']
    cookies = 'ASP.NET_SessionId=mdxoe1kun50hn3erw2pkvglx; ShowGuizhe=1; WebUrl=PorductsDetails.aspx'

    def __init__(self, limit=None, *args, **kwargs):
        super(YanQitzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.yanqicapital.com/Show_html/aspx/PorductsDetails.aspx',
                'ref': None
            }
        ]

        yield self.request_next(fps)

    def parse_fund(self, response):
        urls = response.css("ul.hidden_products>li>a::attr(href)").extract()
        for url in urls:
            self.ips.append({
                'url': 'http://www.yanqicapital.com/Show_html/aspx/' + url,
                'ref': None
            })

        yield self.request_next()

    def parse_item(self, response):
        nvList = response.css("ul.list>li")
        for nv in nvList:
            nvInfo = nv.xpath("span/text()").extract()
            # print(nvInfo[2])
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = nvInfo[0]

            statistic_date = nvInfo[1]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = nvInfo[2]
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = None
            yield item
        yield self.request_next()
