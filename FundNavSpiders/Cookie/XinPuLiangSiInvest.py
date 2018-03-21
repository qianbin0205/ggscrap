from datetime import datetime
from urllib.parse import urljoin
import re
import json
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class XinPuLiangSiInvestSpider(GGFundNavSpider):
    name = 'XinPuLiangSiInvest'
    sitename = '北京信朴量思投资'
    channel = '投资顾问'
    allowed_domains = ['http://www.simplexfund.com']

    username = '点点'
    password = '123456'
    cookies = 'ASPSESSIONIDQCTDCBBQ=DEGHNBDCIMHCODKAEBKGDOCO; __51cke__=; __tins__19385098=%7B%22sid%22%3A%201521297499743%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201521299299743%7D; __tins__19312452=%7B%22sid%22%3A%201521297499877%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201521299299877%7D; __51laig__=4'

    def __init__(self, limit=None, *args, **kwargs):
        super(XinPuLiangSiInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        self.fps = [
            {'url': 'http://www.simplexfund.com/touzi_pro.asp?smallclassid=10'},
            {'url': 'http://www.simplexfund.com/js/fund_base.js'}
        ]
        yield self.request_next()

    def parse_fund(self, response):
        if 'classid=10' in response.url:
            href_list = response.css('span.STYLE4 a::attr(href)').extract()
            for ips_href in href_list:
                if '1517' in ips_href or '1518' in ips_href:
                    self.ips.append({
                        'url': urljoin(self.allowed_domains[0], ips_href),
                        'ref': response.url
                    })

        elif 'fund_base.js' in response.url:
            name_reg = re.compile(r'\sshort_name\s{0,2}:\s{0,2}"(\w*)",', re.DOTALL)
            date_reg = re.compile(r'\sdates\s{0,2}:\s{0,2}(\w*),', re.DOTALL)
            value_reg = re.compile(r'\svalues\s{0,2}:\s{0,2}(\w*)', re.DOTALL)

            name_list = name_reg.findall(response.text)
            date_list = date_reg.findall(response.text)
            value_list = value_reg.findall(response.text)
            self.ips.append({
                'url': 'http://www.simplexfund.com/js/fund_data.js',
                'ref': response.url,
                'ext': {
                    'info_all': zip(name_list, date_list, value_list)
                }
            })

        yield self.request_next()

    def parse_item(self, response):
        into_item = []
        if 'asp' in response.url:
            nav_name_reg = re.compile('titile=\W{0,1}(.*?)\W{0,1};', re.DOTALL)
            nav_date_reg = re.compile('dates=\W{0,1}(\[.*?\]);', re.DOTALL)
            nav_value_reg = re.compile('values=\W{0,1}(\[.*?\]);', re.DOTALL)
            text = ''.join(response.css('span.STYLE3 ::text').extract())
            fund_name = nav_name_reg.findall(text)[0]
            date_list = json.loads(nav_date_reg.findall(text)[0])
            nav_list = json.loads(nav_value_reg.findall(text)[0])
            into_item.append({fund_name: zip(date_list, nav_list)})

        elif 'fund_data.js' in response.url:
            info_all = response.meta['ext']['info_all']
            for fund_name, date_key, value_key in info_all:
                nav_date_reg = re.compile('var %s\W{0,5}(\[.*?\]);' % date_key, re.DOTALL)
                nav_value_reg = re.compile('var %s\W{0,5}(\[.*?\]);' % value_key, re.DOTALL)
                date_list = json.loads(nav_date_reg.findall(response.text)[0])
                nav_list = json.loads(nav_value_reg.findall(response.text)[0])
                into_item.append({fund_name: zip(date_list, nav_list)})

        for i in into_item:
            for k, v in i.items():
                fund_name = k
                for date, nav in v:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(date, '%Y%m%d')
                    item['nav'] = float(nav)
                    yield item

        yield self.request_next()
