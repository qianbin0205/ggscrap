import re
import json
from scrapy import Request
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from datetime import datetime
from scrapy import Selector

class DiyichuangyeSecuritiesManagementSpider(GGFundNavSpider):
    name = 'FundNav_DiyichuangyeSecuritiesManagement'
    sitename = '第一创业证券资管'
    channel = '券商资管净值'
    allowed_domains = ['firstcapital.com.cn']

    username = '18603799126'
    password = '123456'
    cookies = 'JSESSIONID=abcfWVkBJAoBM_-SIgbfw'

    start_urls = []
    fps = [
        {
            'url': 'https://www.firstcapital.com.cn/main/ycyw/zcgl/qxcp/jhzcgljh/jhcp/AE0003/cpgk.html',
            'ref': 'https://www.firstcapital.com.cn/main/ycyw/zcgl/zgdt/ssdt/index.html'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(DiyichuangyeSecuritiesManagementSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.firstcapital.com.cn/main/index/index.html', callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        divFirsts = response.xpath('//div[@class="side_sub01"]')
        divSeconds = divFirsts[1].xpath('./div')
        divThrees = divSeconds[1].xpath('./div')
        divs = divThrees[0].xpath('./div')
        for div in divs:
            fund_hrefs = div.xpath('./a')
            for fund_href in fund_hrefs:
                href = fund_href.xpath('./@href').extract_first()
                fund_name = fund_href.xpath('./text()').extract_first()
                #self.logger.info("地址:"+href)
                fund_code = href.rsplit('/',1)[0].rsplit('/',1)[1]
                ips.append({
                    'url': 'https://www.firstcapital.com.cn/servlet/json',
                    'ref': response.url,
                    'form': {'funcNo':'904317','fundcode':fund_code,'numPage':'15','page':'1'},
                    'headers': {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                    },
                    'ext': {'fund_code':fund_code,'fund_name':fund_name}
                })

        yield self.request_next([], ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']
            ext = response.meta['ext']

            if 'fund_code' in ext:
                fund_code = ext['fund_code']
                fund_name = ext['fund_name']
                totalRows = json.loads(response.text)['results'][0]['totalRows']
                ips.append({
                    'url': 'https://www.firstcapital.com.cn/servlet/json',
                    'ref': '//www.firstcapital.com.cn/main/ycyw/zcgl/qxcp/jhzcgljh/jhcp/AE0003/cpgk.html',
                    'form': {'funcNo': '904317', 'fundcode': fund_code, 'numPage': str(totalRows), 'page': '1'},
                    'headers': {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                    },
                    'ext': {'details_all': 'true','fund_name':fund_name}
                })

            if 'details_all' in ext:
                fund_name = ext['fund_name']
                json_text = json.loads(response.text)
                results ={}
                result = {}
                datas = {}
                if 'results' in json_text:
                    results = json_text['results']
                if len(results) !=0:
                    result = results[0]
                if 'data' in result:
                    datas = result['data']
                if len(datas) != 0:
                    for data in datas:
                        #self.logger.info('基金:' + fund_name)
                        item = GGFundNavItem()
                        item['sitename'] = self.sitename
                        item['channel'] = self.channel
                        item['url'] = response.url

                        fundName = data['fundnm']
                        if fundName is not None and fundName != '':
                          item['fund_name'] = fundName
                        else:
                            item['fund_name'] = fund_name

                        statistic_date = data['settledate']
                        statistic_date = str(statistic_date).split(" ")[0] if statistic_date is not None else None
                        statistic_date = datetime.strptime(statistic_date, '%Y%m%d')
                        item['statistic_date'] = statistic_date

                        if 'nav' in data:
                            nav = data['nav']
                            nav = re.search(r'([0-9.]+)', str(nav))
                            nav = nav.group(0) if nav is not None else None
                            item['nav'] = float(nav)  if nav is not None else None

                        if 'sumofnav' in data:
                            added_nav = data['sumofnav']
                            added_nav = re.search(r'([0-9.]+)', str(added_nav))
                            added_nav = added_nav.group(0) if added_nav is not None else None
                            item['added_nav'] = float(added_nav)  if added_nav is not None else None

                        yield item

            yield self.request_next(fps, ips)