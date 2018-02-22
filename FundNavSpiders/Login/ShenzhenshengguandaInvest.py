import re
import json
from scrapy import Request
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ShenzhenshengguandaInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShenzhenshengguandaInvest'
    sitename = '深圳盛冠达资产投资'
    channel = '投顾净值'
    allowed_domains = ['sz-sgd.com']

    username = '18602199319'
    password = 'yadan0319'

    start_urls = []
    fps = [
        {
            'url': 'http://www.sz-sgd.com/Product.aspx',
            'ref': 'http://www.sz-sgd.com/'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(ShenzhenshengguandaInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.sz-sgd.com/Default.aspx', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.sz-sgd.com/User.ashx',
                          formdata={'username': '18602199319',
                                    'password': 'yadan0319',
                                    'r':'0.9917246479356379',
                                    'type': 'login',
                                    },
                          meta={
                              'handle_httpstatus_list': [302],
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        uls = response.xpath('//ul[@class="fund_li"]')
        for ul in uls:
            lis = ul.xpath('./li')
            for li in lis:
                fund_name = li.xpath('./div[@class="fund_name"]/h3/a/text()').extract_first()
                href = li.xpath('./div[@class="fund_name"]/h3/a/@href').extract_first()
                url = urljoin(get_base_url(response), href)
                ips.append({
                    'url': url,
                    'ref': response.url,
                    'ext':{'fund_name':fund_name}
                })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']
            ext = response.meta['ext']
            fund_name = ext['fund_name']
            regex_start1 = re.compile('var report =.*]\";')
            content = regex_start1.findall(response.text)
            content = content[0].split('[')[1].split(']')[0]
            content = '['+content.replace("\\\"","\"")+']'
            datas = json.loads(content)
            for data in datas:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url

                item['fund_name'] = fund_name

                statistic_date = str(data['y'])+str(data['m'])+str(data['d'])
                statistic_date = str(statistic_date) if statistic_date is not None else None
                statistic_date = datetime.strptime(statistic_date, '%Y%m%d')
                item['statistic_date'] = statistic_date

                nav = data['n']
                nav = re.search(r'([0-9.]+)', str(nav))
                nav = nav.group(0) if nav is not None else None
                item['nav'] = float(nav) if nav is not None else None

                added_nav = data['t']
                added_nav = re.search(r'([0-9.]+)', str(added_nav))
                added_nav = added_nav.group(0) if added_nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item

            yield self.request_next(fps, ips)