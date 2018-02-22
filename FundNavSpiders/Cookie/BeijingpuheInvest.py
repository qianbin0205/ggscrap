import re
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class BeijingpuheInvestSpider(GGFundNavSpider):
    name = 'FundNav_BeijingpuheInvest'
    sitename = '北京朴禾投资'
    channel = '投资顾问'
    allowed_domains = ['pureinvt.com']

    username = '15090191207'
    password = '123456'
    cookies = 'PHPSESSID=q414hljauc4taruoca85lg1uc5'

    start_urls = []
    fps = [
        {
            'url': 'http://www.pureinvt.com/product/list?id=5',
            'ref': 'http://www.pureinvt.com/product/list'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(BeijingpuheInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.pureinvt.com/', callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        last_url = response.xpath('//ul[@class="yiiPager"]/li[@class="last"]/a/@href').extract_first()
        href = last_url.split('&')[0]
        last_page = last_url.split('&')[1].split('=')[1]
        for page in range(1,int(last_page)+1):
            url = href + '&page='+str(page)
            url = urljoin(get_base_url(response), url)
            ips.append({
                'url': url,
                'ref': response.url,
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']

            datas = response.xpath('//div[@class="listBox clear"]/table/tbody/tr')
            for data in datas[1:]:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = data.xpath('./td[1]/text()').extract_first()

                statistic_date = data.xpath('./td[5]/text()').extract_first()
                statistic_date = str(statistic_date) if statistic_date is not None else None
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['statistic_date'] = statistic_date

                nav = data.xpath('./td[2]/text()').extract_first()
                nav = re.search(r'([0-9.]+)', str(nav))
                nav = nav.group(0) if nav is not None else None
                item['nav'] = float(nav) if nav is not None else None

                add_nav = data.xpath('./td[3]/text()').extract_first()
                add_nav = re.search(r'([0-9.]+)', str(add_nav))
                add_nav = add_nav.group(0) if add_nav is not None else None
                item['added_nav'] = float(add_nav) if add_nav is not None else None

                yield item

            yield self.request_next(fps, ips)