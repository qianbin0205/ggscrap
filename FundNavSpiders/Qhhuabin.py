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

    # def start_requests(self):
    #     yield FormRequest(url='http://passport.simuwang.com/index.php?',
    #                       formdata={'m': 'Passport',
    #                                 'c': 'auth',
    #                                 'a': 'login',
    #                                 'rz_cback': 'jQuery1124016502842937214734_1515486948858',
    #                                 'type': 'login',
    #                                 'name': '18637946652',
    #                                 'pass': '870301',
    #                                 'reme': '1',
    #                                 'rn': '1',
    #                                 '_': '1515486948859'},
    #                       callback=self.parse_login)
    #
    # def parse_login(self, response):
    #     fps = [
    #         {
    #             'url': 'http://www.qhhscapital.com/index.asp',
    #             'ref': None,
    #         }
    #     ]
    #
    #     yield self.request_next(fps, [])

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.qhhscapital.com/index.asp',
                'ref': None,
                'username': '18637946652',
                'password': '870301',
                # 'cookies': 'td_cookie=11049241; guest_id=1501155840; PHPSESSID=ms0psbtosmp81qp2m33b59uqc4; stat_sessid=84ipha95t6mhqrtvnp9omfq5l6; regsms=1515461496000; LXB_REFER=www.qhhscapital.com; PHPSESSID=skn6nbs9klupuacd0nv3j03ta3; smppw_tz_auth=1; had_quiz_55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44=1515486491000; had_quiz_55709=1515486843000; http_tK_cache=5c5aabce50d07957bb3f6eb7bb4e37838e3e511d; cur_ck_time=1515486985; ck_request_key=%2Bu6zMFNq6xndIAtj4vrJqqx2obhDItylUYXtpBqpG3A%3D; passport=55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Duser_18637946652; rz_rem_u_p=R%2Fd5WJ8A8gpz3acuDsHFcP37m7DA1PHOfrTLMq53UjY%3D%24yRhNbzMXlnO558gXy6wcxCez9c56HPqsFpGHYyAYgHM%3D; autologin_status=0; rz_token_6658=5f63e6ac68d6a83283507cde3c4ff47a.1515492331; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1515490562,1515492456,1515492649,1515492668; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1515492668'
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.xpath("//tbody/tr/td[1]/p/span/a")

        for fund in funds:
            fund_name = fund.css('::text').extract_first()
            fund_id = fund.css('::attr(href)').re_first(r'product\/(\S+)\.html')
            url = fund.css('::attr(href)').extract_first()
            url = urljoin(get_base_url(response), url)
            ips.append({
                'pg': 1,
                'url': lambda
                    pg: 'http://dc.simuwang.com/fund/getNavList.html?id=' + fund_id + '&muid=55709&page=' + str(pg),
                'ref': url,
                'ext': {'fund_name': fund_name},
                'cookies': 'td_cookie=11049250; guest_id=1501155840; PHPSESSID=ms0psbtosmp81qp2m33b59uqc4; stat_sessid=84ipha95t6mhqrtvnp9omfq5l6; regsms=1515461496000; LXB_REFER=www.qhhscapital.com; PHPSESSID=skn6nbs9klupuacd0nv3j03ta3; smppw_tz_auth=1; had_quiz_55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44=1515486491000; had_quiz_55709=1515486843000; http_tK_cache=5c5aabce50d07957bb3f6eb7bb4e37838e3e511d; cur_ck_time=1515486985; ck_request_key=%2Bu6zMFNq6xndIAtj4vrJqqx2obhDItylUYXtpBqpG3A%3D; passport=55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Duser_18637946652; rz_rem_u_p=R%2Fd5WJ8A8gpz3acuDsHFcP37m7DA1PHOfrTLMq53UjY%3D%24yRhNbzMXlnO558gXy6wcxCez9c56HPqsFpGHYyAYgHM%3D; autologin_status=0; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1515493807,1515493810,1515496559,1515498005; rz_token_6658=c1e37b589b9ac08579ce3049f02ed318.1515498005; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1515499098'
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

        pagecount = json.loads(response.text)['pager']['pagecount']
        if pg < pagecount:
            ips.append({
                'pg': pg + 1,
                'url': url,
                'ref': response.request.headers['Referer'],
                # 'cookies': 'td_cookie=11049241; guest_id=1501155840; PHPSESSID=ms0psbtosmp81qp2m33b59uqc4; stat_sessid=84ipha95t6mhqrtvnp9omfq5l6; regsms=1515461496000; LXB_REFER=www.qhhscapital.com; PHPSESSID=skn6nbs9klupuacd0nv3j03ta3; smppw_tz_auth=1; had_quiz_55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44=1515486491000; had_quiz_55709=1515486843000; http_tK_cache=5c5aabce50d07957bb3f6eb7bb4e37838e3e511d; cur_ck_time=1515486985; ck_request_key=%2Bu6zMFNq6xndIAtj4vrJqqx2obhDItylUYXtpBqpG3A%3D; passport=55709%09user_18637946652%09BAFcXwgHVlEBAgIBBQ5WVARYAVMLBFJSAFcGDg9SVwU%3D94f932ae44; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Duser_18637946652; rz_rem_u_p=R%2Fd5WJ8A8gpz3acuDsHFcP37m7DA1PHOfrTLMq53UjY%3D%24yRhNbzMXlnO558gXy6wcxCez9c56HPqsFpGHYyAYgHM%3D; autologin_status=0; rz_token_6658=5f63e6ac68d6a83283507cde3c4ff47a.1515492331; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1515490562,1515492456,1515492649,1515492668; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1515492668'

            })

        yield self.request_next(fps, ips)
