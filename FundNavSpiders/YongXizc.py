import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YongXizcSpider(GGFundNavSpider):
    name = 'FundNav_YongXizc'
    sitename = '浙江永禧投资'
    channel = '投资顾问'
    allowed_domains = ['www.yxassets.com']

    start_urls = ['http://www.yxassets.com/product']
    url = 'http://www.yxassets.com'

    def __init__(self, limit=None, *args, **kwargs):
        super(YongXizcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.yxassets.com/product',
                'ref': None,
            }
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        funds = response.css('div.product_section>div.left_box>ul>li>a')
        ips = []
        for fund in funds:
            fundName = fund.xpath('text()').extract()[0]
            fundLink = fund.xpath('@href').extract()[0]
            ips.append(
                    {
                        'url': self.url + fundLink,
                        'ref': response.url,
                        'headers': {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                        },
                        'ext': {'fund_name': fundName}
                    }
            )
        yield self.request_next([], ips)

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        navTable = response.css('div.right_box>div.content>table.table')
        navInfo = navTable.xpath('tr[1]/td[2]/text()')
        navArray = navInfo.extract()[0].split('（')

        if len(navArray) > 1:
            nav = navArray[0]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = navArray[1].replace('截止', '').replace('：', '').replace('）', '')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')

            item['nav'] = float(nav)
            item['added_nav'] = None
            yield item
        yield self.request_next()
