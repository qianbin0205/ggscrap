# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class XiamenTrustSpider(GGFundNavSpider):
    name = 'FundNav_XiamenTrust'
    sitename = '厦国投'
    channel = '发行机构'
    allowed_domains = ['www.xmitic.com']
    start_urls = ['http://www.xmitic.com/']

    username = 'qzm'
    password = 'qzm123'
    cookies = 'td_cookie=11049118; ant_stream_5a4fa6a5e96dc=1517476782/3942334202; bow_stream_5a4fa6a5e96dc=13; myCookie=; _siteUp=1; ASP.NET_SessionId=rl50x0454w4tr555hglwfb45'

    def __init__(self, limit=None, *args, **kwargs):
        super(XiamenTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        ips = [
            {
                'url': 'https://www.xmitic.com/jingzhi.aspx',
                'ref': 'https://www.xmitic.com/usercenter.aspx'
            }
        ]
        yield self.request_next([], ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        rows = response.xpath("//div[@class='textArea mt-20']/table/tbody/tr")[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = row.xpath("./td[3]/text()").extract_first()

            statistic_date = row.xpath("./td[2]/text()").extract_first().replace('/', '-')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            total_nav = row.xpath("./td[4]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['total_nav'] = float(total_nav) if total_nav is not None else None

            share = row.xpath("./td[5]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['share'] = float(share) if share is not None else None

            nav = row.xpath("./td[6]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row.xpath("./td[7]").re_first(r'>\s*?([0-9.]+)\s*?<')
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url is not None and next_url != 'javascript:void(0)':
            url = urljoin(get_base_url(response), next_url)
            ips.append({
                'url': url,
                'ref': response.url
            })

        yield self.request_next(fps, ips)
