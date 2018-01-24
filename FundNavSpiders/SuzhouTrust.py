import re
from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy.utils.response import  get_base_url
from urllib.parse import  urljoin


class SuzhouTrustSpider(GGFundNavSpider):
    name = 'FundNav_SuzhouTrust'
    sitename = '苏州信托'
    channel = '发行机构'
    allowed_domains = ['trustsz.com']
    start_urls = ['http://www.trustsz.com/index.html']

    def __init__(self, limit=None, *args, **kwargs):
        super(SuzhouTrustSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.trustsz.com/index.html',
                'ref': 'www.trustsz.com/'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        trs = response.xpath("//div[@class='J_webmain_box_cnt']/table/tr")
        for tr in trs[1:]:
            url = tr.xpath("./td[1]/a/@href").extract_first()
            ips.append({
                'url':url,
                'ref':response.url
            })

        yield self.request_next([], ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        nextUrl = response.xpath("//span[@class='page_next page_abled']/a/@href").extract_first()
        nextUrl = urljoin(get_base_url(response), nextUrl)
        refUrl = response.url
        if nextUrl !=''and refUrl != nextUrl:
            ips.append({
                'url': nextUrl,
                'ref': response.url
            })
        trs = response.xpath("//div[@class='k1']/table/tbody/tr")
        for tr in trs[2:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = tr.xpath("./td[1]/text()").extract_first()

            statistic_date = tr.xpath("./td[2]/text()").extract_first().strip()
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['statistic_date'] = statistic_date

            nav = tr.xpath("./td[3]/text()").extract_first().strip()
            nav = re.search(r'([0-9.]+)', nav)
            nav = nav.group(0) if nav is not None else None
            item['nav'] = float(nav) if nav is not None else None

            yield item

        yield self.request_next(fps, ips)