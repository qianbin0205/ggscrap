# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class PinzhengFundSpider(GGFundNavSpider):
    name = 'FundNav_PinzhengFund'
    sitename = '品正资产'
    channel = '投资顾问'
    allowed_domains = ['www.purezenfund.com']
    start_urls = ['http://www.purezenfund.com/']
    cookies = 'modal_cookie=1; ci_session=a%3A7%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22f6e9436e76a3dcae85ce5f114cf7bd84%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22203.110.179.245%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A114%3A%22Mozilla%2F5.0+%28Windows+NT+6.1%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F63.0.3239.108+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1516087873%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22userInfo%22%3Ba%3A11%3A%7Bs%3A2%3A%22id%22%3Bs%3A2%3A%2213%22%3Bs%3A8%3A%22username%22%3Bs%3A11%3A%2215838535216%22%3Bs%3A8%3A%22password%22%3Bs%3A32%3A%229524ef7b0c9109f74d7c7015e0ec37ca%22%3Bs%3A8%3A%22truename%22%3Bs%3A9%3A%22%E6%9D%8E%E4%BA%9A%E6%A5%A0%22%3Bs%3A6%3A%22mobile%22%3Bs%3A11%3A%2215838535216%22%3Bs%3A5%3A%22email%22%3BN%3Bs%3A7%3A%22address%22%3BN%3Bs%3A3%3A%22sex%22%3Bs%3A1%3A%221%22%3Bs%3A8%3A%22reg_time%22%3Bs%3A10%3A%221475214549%22%3Bs%3A10%3A%22login_time%22%3Bs%3A10%3A%221516085964%22%3Bs%3A9%3A%22status_id%22%3Bs%3A1%3A%221%22%3B%7Ds%3A6%3A%22isRisk%22%3Bb%3A1%3B%7D128cef92df2f3d2a319593612bc3f249; td_cookie=11049135'
    username = '15838535216'
    password = '050835'

    def __init__(self, limit=None, *args, **kwargs):
        super(PinzhengFundSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.purezenfund.com/?c=product&m=lists',
                'ref': 'http://www.purezenfund.com/?c=product&m=detail&id=9'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        urls = response.xpath("//div[@class='leftBar fl']/div[2]/ul/li/a/@href").extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        fund_name = response.xpath("//h3[@class='mgb20']/text()").extract_first()
        rows = response.xpath("//div[@class='cont_box'][2]/table/tbody/tr")
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.css('td:nth-child(2)').re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.css('td:nth-child(3)::text').extract_first()
            item['nav'] = float(nav)if nav is not None else None

            added_nav = row.css('td:nth-child(4)::text').extract_first()
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            yield item

        yield self.request_next(fps, ips)
