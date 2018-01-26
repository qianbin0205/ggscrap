import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class ChuangYingtzSpider(GGFundNavSpider):
    name = 'FundNav_ChuangYingtz'
    sitename = '创赢投资'
    channel = '产品净值'
    allowed_domains = ['www.cymm169.com']
    start_urls = ['http://www.cymm169.com/cpjz.asp?id=1']
    url = 'http://www.cymm169.com/cpjz.asp'

    def __init__(self, limit=None, *args, **kwargs):
        super(ChuangYingtzSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.cymm169.com/cpjz.asp?id=1',
                'ref': None,
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        # print(response.body)

        Funds = response.xpath('//td[@background="images/navmenubg01.GIF"]')
        for eachFund in Funds:
            fundLink = eachFund.xpath('a/@href').extract()[0]
            # print(fundLink)
            yield Request(self.url + fundLink, callback=self.parse_nv_link)

    def parse_nv_link(self, response):
        fps = []
        ips = []
        # print(fps)
        # print(ips)

        fundItem = response.xpath('//div[@class="cpjzab"]')[2]
        # print(fundItem)
        fundNvLink = fundItem.xpath('a/@href').extract()[0]
        url = self.url + fundNvLink
        ips.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = []
        ips = []

        nvTable = response.xpath('//table[@id="table9"]')
        nvList = nvTable.xpath('tr')[1:]

        curSelItem = response.xpath('//div[@class="cpjzab"][1]')
        fundNameTable = curSelItem.xpath('parent::*').xpath('parent::*').xpath('parent::*').xpath('preceding-sibling::*[1]')
        fundName = fundNameTable.xpath('tr/td/a/text()').extract()[0]

        for eachNv in nvList:
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fundName

            statistic_date = eachNv.xpath('td/text()').extract()[1]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = eachNv.xpath('td/text()').extract()[2]
            item['nav'] = float(nav) if nav is not None else None

            added_nav = eachNv.xpath('td/text()').extract()[3]
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item
            # fundNvDate = eachNv.xpath('td/text()').extract()[1]
            # fundNvValue = eachNv.xpath('td/text()').extract()[2]
            # fundNvTotelValue = eachNv.xpath('td/text()').extract()[3]
            # print(fundNvDate)
            # print(fundNvValue)
            # print(fundNvTotelValue)

        nvPageTable=nvTable.xpath('following-sibling::*')[0]
        # print(nvPageTable)
        nextPage=nvPageTable.xpath('tr/td/a')[2]
        # print(nextPage)
        nextPageUrl=nextPage.xpath('@href').extract()[0]
        # print(nextPageUrl)
        url = self.url + nextPageUrl
        ips.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(fps, ips)
