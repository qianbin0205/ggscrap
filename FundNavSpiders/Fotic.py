# -*- coding: utf-8 -*-

from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
import json
import config


class FoticSpider(GGFundNavSpider):
    name = 'FundNav_Fotic'
    sitename = '外贸信托'
    channel = '信托净值'
    allowed_domains = ['www.fotic.com.cn']

    proxy = config.proxy
    start_urls = []
    fps = [
        {
            'pg': 1,
            'url': 'http://www.fotic.com.cn/DesktopModules/Globalstech/ProductJZ/GetJsonResult.ashx',
            'form': {'programName': '', 'sDate': '', 'eDate': '', 'pageNo': lambda pg: str(pg), 'pageSize': '500'},
            'headers': {'Accept': 'application/json, text/javascript, */*; q=0.01'},
            'ref': 'http://www.fotic.com.cn/8097.html',
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(FoticSpider, self).__init__(limit, *args, **kwargs)

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = json.loads(response.text)['result']
        for fund in funds:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = 'http://www.fotic.com.cn/8074.html?i=3'
            item['fund_name'] = fund['projectnameshort']

            statistic_date = fund['date']
            statistic_date = statistic_date.strip()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = fund['netvalue']
            item['nav'] = float(nav) if nav else nav

            yield item

        pg = response.meta['pg']
        form = response.meta['form']
        url = response.meta['url']
        pagesize = int(form['pageSize'])
        totalpage = json.loads(response.text)['totalCount']/pagesize
        if pg < totalpage:
            fps.append({
                'pg': pg+1,
                'url': url,
                'form': form,
                'headers': {'Accept': 'application/json, text/javascript, */*; q=0.01'},
                'ref': 'http://www.fotic.com.cn/8097.html'
            })

        yield self.request_next()
