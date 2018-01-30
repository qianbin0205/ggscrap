import re
import json
from scrapy import Request
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from datetime import datetime
from scrapy import Selector
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ChiyingInvestSpider(GGFundNavSpider):
    name = 'FundNav_ChiyingInvest'
    sitename = '持赢投资'
    channel = '投顾净值'
    allowed_domains = ['chiyingfund.com']

    username = '350402197902120017'
    password = 'ZYYXSM123'

    start_urls = []
    fps = [
        {
            'url': 'http://www.chiyingfund.com/index.php?s=/Home/Page/member.html',
            'ref': 'http://www.chiyingfund.com/index.php?s=/Home/Index/index.html'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(ChiyingInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.chiyingfund.com/index.php?s=/Home/Index/index.html', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.chiyingfund.com/index.php?s=/Home/Index/gologin.html',
                          formdata={'username': '350402197902120017',
                                    'password': 'ZYYXSM123'
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
        ext = response.meta['ext']

        sel =  Selector(text=response.text)
        products = sel.xpath('//ul[@class="ziye_left_menu_box"]/li/ul[@class="erji"]/li')
        for product in products:
            fund_name = product.xpath('./a/text()').extract_first()
            li_class = product.xpath('./@class').extract_first()
            on_type = 'close_open'
            form={}
            if li_class == 'on':
                if 'type' in ext:
                    url = 'http://www.chiyingfund.com/index.php?s=/Home/Page/member_open.html'
                else:
                    url = 'http://www.chiyingfund.com/index.php?s=/Home/Page/member.html'
                on_type = 'on'
            else:
                pid = product.xpath('./a/@pid').extract_first()
                url = 'http://www.chiyingfund.com/index.php?s=/Home/Operate/nochange.html'
                form = {'pid':pid}
            ips.append({
                'url': url,
                'ref': response.url,
                'form':form,
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                },
                'ext': {'on_type': on_type,'fund_name':fund_name}
            })

        if 'type' not in ext:
            fps = [
                {
                    'url': 'http://www.chiyingfund.com/index.php?s=/Home/Page/member_open.html',
                    'ref': response.url,
                    'ext': {'type': 'open'}
                }
            ]
        yield self.request_next(fps, ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']
            ext = response.meta['ext']
            on_type = ext['on_type']
            fund_name = ext['fund_name']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            if on_type == 'on':
                statistic_date = response.xpath('//div[@class="achievement_final_box"]/div[@class="top clearfix"]/div[@class="intro right"]/table/tr[1]/td[2]/text()').extract_first()
                statistic_date = str(statistic_date) if statistic_date is not None else None
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['statistic_date'] = statistic_date

                added_nav = response.xpath(
                    '//div[@class="achievement_final_box"]/div[@class="top clearfix"]/div[@class="intro right"]/table/tr[5]/td[2]/text()').extract_first()
                added_nav = re.search(r'([0-9.]+)', str(added_nav))
                added_nav = added_nav.group(0) if added_nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item
            else:
                product = json.loads(response.text)['result']
                statistic_date = product['endtime']
                statistic_date = str(statistic_date) if statistic_date is not None else None
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['statistic_date'] = statistic_date

                added_nav = product['total_networth']
                added_nav = re.search(r'([0-9.]+)', str(added_nav))
                added_nav = added_nav.group(0) if added_nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item
            yield self.request_next(fps, ips)