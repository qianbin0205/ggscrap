# -*- coding: utf-8 -*-
from datetime import datetime
import re
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class BaiShiAssetsSpider(GGFundNavSpider):
    name = 'FundNav_BaiShiAssets'
    sitename = '白石资产'
    channel = '投资顾问'
    allowed_domains = ['http://www.whiterock.cn']
    # 并不需要用账号密码，只是记录一下
    txtUserName = '朵朵'
    password = 'bs123456'

    def __init__(self, *args, **kwargs):
        super(BaiShiAssetsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.whiterock.cn/index.php',
            }
        ]
        yield self.request_next(fps)

    def parse_fund(self, response):
        ips = response.meta['ips']
        fund_ids = response.xpath('//select[@name = "select"]//option//@value').extract()
        # 净值每个产品都存放在单独的页面,通过fund_id的更改分别进入
        for fund_id in fund_ids:
            url = 'http://www.whiterock.cn/_api.php?id=%d&type=1' % int(fund_id)
            ips.append({
                'url': url,
                'ref': response.url
            })
        yield self.request_next(ips)

    def parse_item(self, response):
        fundname = re.findall('产品名称：\w*', response.text)[0].replace('产品名称：', '')
        data_list = ''.join('@'.join(response.xpath('.//text()').extract()).split())
        navs = json.loads(json.loads(data_list)['yValue'])
        dates = json.loads(data_list)['xValue'].replace('[', '').replace(']', '').replace('\'', '').split(',')

        for nav, date in zip(navs, dates):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fundname
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(nav)
            yield item

        yield self.request_next()
