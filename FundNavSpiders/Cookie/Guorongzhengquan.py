import re
import json
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class GuorongzhengquanSpider(GGFundNavSpider):
    name = 'FundNav_GuorongzhengquanInvest'
    sitename = '国融证券'
    channel = '券商资管净值'
    allowed_domains = ['mall.grzq.com']

    username = '13916427906'
    password = 'ZYYX13'
    cookies = 'JSESSIONID=abcdXQWUItzdq-05YWngw'

    start_urls = []
    fps = [
        {
            'url': 'https://mall.grzq.com/servlet/json?funcNo=2000015&currentPage=1&numPerPage=5',
            'ref': 'https://mall.grzq.com/osoa/views/mall/zgcpy/index.html'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(GuorongzhengquanSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url='https://mall.grzq.com/', callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        if 'totalRows'not in ext:
            totalRows = json.loads(response.text)['results'][0]['totalRows']
            url = 'https://mall.grzq.com/servlet/json?funcNo=2000015&currentPage=1&numPerPage='+str(totalRows)
            fps.append({
                'url': url,
                'ref': response.url,
                'ext':{'totalRows':totalRows}
            })
        else:
            datas = json.loads(response.text)['results'][0]['data']
            for data in datas:
                fund_code = data['p_cpdm']
                url ='https://mall.grzq.com/osoa/views/mall/cpxq/zgcpxq/'+fund_code+'/index.html'
                ips.append({
                    'url': url,
                    'ref': response.url,
                })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']
            ext = response.meta['ext']

            if 'fund_code' not in ext:
                fund_name = response.xpath('//div[@id="cp_bottom"]/ul[@class="xx_list"]/li[1]/em/text()').extract_first()
                url = response.url
                fund_code = url.rsplit('/',2)[1]
                fund_url = 'https://mall.grzq.com/servlet/json?funcNo=2000024&productcode='+str(fund_code)
                ips.append({
                    'url': fund_url,
                    'ref': response.url,
                    'ext':{'fund_code':fund_code,'fund_name':fund_name}
                })
            else:
                fund_name = ext['fund_name']
                datas = json.loads(response.text)['results']
                for data in datas:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name

                    statistic_date = data['value_date']
                    statistic_date = str(statistic_date) if statistic_date is not None else None
                    statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                    item['statistic_date'] = statistic_date

                    nav = data['now_value']
                    nav = re.search(r'([0-9.]+)', str(nav))
                    nav = nav.group(0) if nav is not None else None
                    item['nav'] = float(nav) if nav is not None else None

                    add_nav = data['all_value']
                    add_nav = re.search(r'([0-9.]+)', str(add_nav))
                    add_nav = add_nav.group(0) if add_nav is not None else None
                    item['added_nav'] = float(add_nav) if add_nav is not None else None

                    yield item

            yield self.request_next(fps, ips)