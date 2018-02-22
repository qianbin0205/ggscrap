# -*- coding: utf-8 -*-
import json
from datetime import datetime
from scrapy import FormRequest
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class DongWuSecuritiesSpider(GGFundNoticeSpider):
    name = 'FundNotice_DongWuSecurities'
    sitename = '东吴证券'
    channel = '券商资管公告'
    entry = 'http://www.dwzq.com.cn/page/34'
    allowed_domains = ['www.dwzq.com.cn', 'www.dwjq.com.cn']

    username = '13916427906'
    password = 'ZYYXSM123'

    def __init__(self, *args, **kwargs):
        super(DongWuSecuritiesSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.dwzq.com.cn/api/whatWeDo/login',
                          method='POST',
                          body=b'{"tel":"13916427906","password":"ZYYXSM123","languageFlg":"0"}',
                          headers={
                              'Content-Type': 'application/json;charset=UTF-8'
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        self.lps = [{
            'url': 'http://www.dwzq.com.cn/api/whatWeDo/collectiveFinancingList',
            'headers': {
                'Content-Type': 'application/json;charset=UTF-8'
            },
            'body': '{"currentPage":1,"recordNumber":100,"firstType":"0","languageFlg":"0","secondType":"0"}',
            'ref': response.url,
            'pg': 1
        }]

        yield self.request_next()

    def parse_list(self, response):
        pi = response.meta['pi']
        pg = pi['pg']
        data = json.loads(response.text)['info']
        total_count = int(data['totalCount'])
        total_pg = total_count // 100 if (total_count % 100) == 0 else total_count // 100 + 1
        pg = pg + 1
        if pg <= total_pg:
            self.lps.append({
                'url': 'http://www.dwzq.com.cn/api/whatWeDo/collectiveFinancingList',
                'headers': {
                    'Content-Type': 'application/json;charset=UTF-8'
                },
                'body': '{"currentPage":' + str(pg) + ',"recordNumber":100,"firstType":"0","languageFlg":"0","secondType":"0"}',
                'ref': response.url,
                'pg': pg
            })

        rows = data['list']
        for row in rows:
            product_code = row['productCode']
            url = 'http://www.dwzq.com.cn/api/whatWeDo/financingInfoList'
            self.ips.append({
                'url': url,
                'headers': {'Content-Type': 'application/json;charset=UTF-8'},
                'body': '{"firstType":"","secondType":"","type":"1","productCode":"' + product_code + '","recordID":"","currentPage":1,"recordNumber":100,"languageFlg":"0"}',
                'ref': response.url,
                'pg': 1,
                'ext': {'type': '1', 'product_code': product_code}
            })
            self.ips.append({
                'url': url,
                'headers': {'Content-Type': 'application/json;charset=UTF-8'},
                'body': '{"firstType":"","secondType":"","type":"2","productCode":"' + product_code + '","recordID":"","currentPage":1,"recordNumber":100,"languageFlg":"0"}',
                'ref': response.url,
                'pg': 1,
                'ext': {'type': '2', 'product_code': product_code}
            })
            self.ips.append({
                'url': url,
                'headers': {'Content-Type': 'application/json;charset=UTF-8'},
                'body': '{"firstType":"","secondType":"","type":"3","productCode":"' + product_code + '","recordID":"","currentPage":1,"recordNumber":100,"languageFlg":"0"}',
                'ref': response.url,
                'pg': 1,
                'ext': {'type': '3', 'product_code': product_code}
            })
        yield self.request_next()

    def parse_item(self, response):
        pi = response.meta['pi']
        pg = pi['pg']
        ext = response.meta['ext']
        body_type = ext['type']
        product_code = ext['product_code']
        print(product_code)
        data = json.loads(response.text)['info']
        if data is not None:
            rows = data['list']
            for row in rows:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                if 'fileURL' not in row:
                    continue
                file_url = row['fileURL']
                item['url'] = 'http://www.dwzq.com.cn/wwwfile/file' + file_url
                item['title'] = row['infoTitle']
                publish_time = row['infoDate']
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                yield item

            total_count = int(data['totalCount'])
            total_pg = total_count // 100 if (total_count % 100) == 0 else total_count // 100 + 1
            pg = pg + 1
            if pg <= total_pg:
                self.ips.append({
                    'url': 'http://www.dwzq.com.cn/api/whatWeDo/financingInfoList',
                    'headers': {'Content-Type': 'application/json;charset=UTF-8'},
                    'body': '{"firstType":"","secondType":"","type":"' + body_type + '","productCode":"' + product_code + '","recordID":"","currentPage":1,"recordNumber":100,"languageFlg":"0"}',
                    'ref': response.url,
                    'pg': pg,
                    'ext': ext
                })

        yield self.request_next()
