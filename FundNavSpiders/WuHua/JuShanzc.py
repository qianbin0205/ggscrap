import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy import FormRequest

class JuShanzcSpider(GGFundNavSpider):
    name = 'FundNav_JuShanzc'
    sitename = '巨杉资产'
    channel = '投资顾问'
    allowed_domains = ['www.grasset.com.cn']
    # start_urls = ['http://derivatives-china.invest.ldtamp.com/pfL.1.201.json']

    def __init__(self, limit=None, *args, **kwargs):
        super(JuShanzcSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.grasset.com.cn/api/login/login',
                      method='post',
                      headers={'Content-Type': 'application/json',
                               'Referer': 'http://www.grasset.com.cn/auth',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'},
                      body=b'{"loginName":"13916427906","password":"123456"}',
                      callback=self.parse_login)

    def parse_login(self, response):
        # print(response.text)
        yield Request(url='http://www.grasset.com.cn/api/product/queryNetValueList',
                      method='post',
                      headers={'Content-Type': 'application/json',
                               'Referer': 'http://www.grasset.com.cn/productNetValueList',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'},
                      body=b'{"auditStatus":"3","productName":"","productType":""}',
                      callback=self.parse_nv_link)

    def parse_nv_link(self, response):
        # print(response.text)
        funds = json.loads(response.text)["data"]["records"]
        # print(funds)
        for fund in funds:
            fundId = fund['productId']
            fundName = fund['productName']
            # print(fundId)
            payload = {"productId": fundId, "pageSize": "20", "pageNumber": "1"}
            yield Request(url='http://www.grasset.com.cn/api/product/netValue/query',
                        method='post',
                        meta={'fundName': fundName},
                        headers={'Content-Type': 'application/json',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'},
                        body=json.dumps(payload),
                        callback=self.parse_item)

    def parse_item(self, response):
        # print(response.text)
        fundName = response.meta['fundName']
        # print(fundName)
        # nvData = json.loads(response.text)["data"]
        # # nValues = json.loads(response.text)["data"]["records"]
        # nvRecordCount = nvData["totalRecordCount"]
        # # print(nvRecordCount)
        # nvRecordList = nvData["records"]
        # for nvRecord in nvRecordList:

