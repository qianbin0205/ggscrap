from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
import re
import time


class BaoChiInvestSpider(GGFundNavSpider):
    name = 'FundNav_BaoChiInvest'
    sitename = '宝驰投资'
    channel = '投顾净值'
    allowed_domains = ['www.hbbctz.com']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'UM_distinctid=161f4e2337b2cb-0f6bd4f5924643-191e7352-1fa400-161f4e2337c5f5; PHPSESSID=5anunpnr3ublebm42jfcdh6v32; CNZZDATA1256459553=276520537-1520231920-http%253A%252F%252Fwww.hbbctz.com%252F%7C1521703190; td_cookie=11048770',

    def __init__(self, limit=None, *args, **kwargs):
        super(BaoChiInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        self.fps = [
            {'url': 'http://www.hbbctz.com/product.php'}
        ]
        yield self.request_next()

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class = "leftbar fl"]//ul//li//@href').extract()
        fund_names = response.xpath('//div[@class = "leftbar fl"]//ul//li//@title').extract()
        for url, fund_name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.hbbctz.com/', url.replace('product.', 'chartdata.').replace('php?c', 'php?'))
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })
        yield self.request_next()

    def parse_item(self, response):
        funds_info = re.findall(r"var jz_date=(.*?)];var hs_date", response.text)[0]
        fund_info = re.findall(r"\[(\d+),(\d{1,2}.\d+)\]", funds_info)
        fund_name = response.meta['ext']['fund_name']
        for i in fund_info:
            fund_date = time.strftime("%Y-%m-%d", time.localtime(int(i[0]) / 1000))
            fund_nav = i[1]
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(fund_nav) if fund_nav is not None else None
            yield item
        yield self.request_next()
