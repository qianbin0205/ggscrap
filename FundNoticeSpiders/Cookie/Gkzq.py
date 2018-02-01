# -*- coding: utf-8 -*-

import json
from datetime import datetime
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class GkzqSpider(GGFundNoticeSpider):
    name = 'FundNotice_Gkzq'
    sitename = '国开证券资管'
    channel = '公告'
    entry = 'http://www.gkzq.com.cn/gkzq/zqyj/zqyjInfoList11.jsp?classid=0001000100040008'
    allowed_domains = ['www.gkzq.com.cn']
    start_urls = []

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'td_cookie=11049162; td_cookie=11049153; JSESSIONID=ArRKgrYKpIjYsT2K6YeP1dWfDwexgWts3dCX8D6chm37cWEboybe!-229239174; ecsn-session=10019f49'

    lps = [
        {
            'url': 'http://www.gkzq.com.cn/gkzq/zqyj/zqyjInfoList11.jsp?classid=0001000100040008',
            'ref': None
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(GkzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        urls = response.xpath("//ul[@id='rewin_list_10']/a/@href").extract()
        for url in urls:
            classid = url.split('=', 1)[1]
            self.ips.append({
                'url': 'http://www.gkzq.com.cn/gkzq/JSONService/rewinJsonInfoListMore_simple.jsp?classid=' + classid + '0003&datalen=500',
                'ref': response.url,
            })
            self.ips.append({
                'url': 'http://www.gkzq.com.cn/gkzq/JSONService/rewinJsonInfoListMore_simple.jsp?classid=' + classid + '0004&datalen=500',
                'ref': response.url,
            })

        yield self.request_next()

    def parse_item(self, response):

        datas = json.loads(response.text)['result']
        for data in datas:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            infoId = data['infoId']
            classid = response.url.split('=', 1)[1].split('&', 1)[0]
            item['url'] = 'http://www.gkzq.com.cn/gkzq/public/infoShow.jsp?classid=' + classid + '&infoid=' + str(infoId)
            item['title'] = data['title']
            publish_time = data['originaltime'][0:10]
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        yield self.request_next()

