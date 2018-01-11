# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import json


class QhhuabinSpider(GGFundNavSpider):
    name = 'FundNav_Qhhuabin'
    sitename = '前海华杉投资'
    channel = '投顾净值'
    allowed_domains = ['www.qhhscapital.com']
    start_urls = ['http://www.qhhscapital.com/']

    def __init__(self, limit=None, *args, **kwargs):
        super(QhhuabinSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://passport.simuwang.com/index.php',
                          formdata={
                                    'name': '18637946652',
                                    'pass': '870301'},
                          callback=self.parse_login)

    def parse_login(self, response):
        print(response.text)
        fps = [
            {
                'url': 'http://www.qhhscapital.com/index.asp',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//tbody/tr/td[1]/p/span/a")

        for fund in funds:
            fund_name = fund.css('::text').extract_first()
            fund_id = fund.css('::attr(href)').re_first(r'product/(\S+).html')
            u = fund.css('::attr(href)').extract_first()
            u = urljoin(get_base_url(response), u)
            ips.append({
                'pg': 1,
                'url': 'http://dc.simuwang.com/fund/getNavList.html',
                'form': {'id': fund_id, 'muid': '55709', 'page': lambda pg: str(pg)},
                'ref': u,
                'ext': {'fund_name': fund_name},
                'cookies': 'td_cookie=11049270; guest_id=1501155840; regsms=1515461496000; smppw_tz_auth=1; had_quiz_55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44=1515486491000; had_quiz_55709=1515486843000; PHPSESSID=lld0v5mclrt8s67rhp639loa64; rz_token_6658=d35c977b5dfec989e3441c0b2d427433.1515636646; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1515564505,1515573393,1515573409,1515636647; LXB_REFER=www.qhhscapital.com; stat_sessid=e946ga3m76p8s0uebup1aa8585; http_tK_cache=f0a1b484fa13ebf7a2b128c05306f7d56fea4db1; cur_ck_time=1515636690; ck_request_key=mhlOji2ojWclsaJs4usWwy2QY0hd8%2Fw6jNYIw6AS7B0%3D; passport=55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Duser_18637946652; rz_rem_u_p=R%2Fd5WJ8A8gpz3acuDsHFcP37m7DA1PHOfrTLMq53UjY%3D%24yRhNbzMXlnO558gXy6wcxCez9c56HPqsFpGHYyAYgHM%3D; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1515636691; autologin_status=0'

            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        pg = response.meta['pg']
        ext = response.meta['ext']
        url = response.meta['url']
        fund_name = ext['fund_name']

        datas = json.loads(response.text)['data']
        for data in datas:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']

            item['fund_name'] = fund_name

            statistic_date = data['d']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = data['n']
            item['nav'] = float(nav)

            added_nav = data['cn']
            item['added_nav'] = float(added_nav)

            yield item
        form = response.meta['form']
        pagecount = json.loads(response.text)['pager']['pagecount']
        if pg < pagecount:
            ips.insert(0, {
                'pg': pg + 1,
                'url': url,
                'form': form,
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
