# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from GGScrapy.items import GGIrcsItem
from GGScrapy.ggspider import GGIrcsSpider
from scrapy.utils.response import get_base_url


class CninfoIrmSpider(GGIrcsSpider):
    name = 'Ircs_CninfoIrm'
    sitename = '深交所互动易'
    channel = '投资者关系互动平台-最新回复'
    entry = 'http://irm.cninfo.com.cn/ircs/sse/sseSubIndex.do?condition.type=7'
    allowed_domains = ['irm.cninfo.com.cn']

    start_urls = []
    lps = [
        {
            'url': 'http://irm.cninfo.com.cn/ircs/interaction/lastRepliesForSzse.do',
            'ref': 'http://irm.cninfo.com.cn/ircs/sse/sseSubIndex.do?condition.type=7'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(CninfoIrmSpider, self).__init__(*args, **kwargs)

    def parse_list(self, response):
        records = response.css('.talkList2>.askBoxOuter')
        for record in records:
            url = record.css('.msgBox .msgCnt a.cntcolor::attr(href)').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': None
            })

        yield self.request_next()

    def parse_item(self, response):
        item = GGIrcsItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url

        author = response.css('.askBoxOuter .userPic .userName::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['author'] = author

        stock_code = response.css('.answerBoxOuter .userPic .comCode>a::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['stock_code'] = stock_code

        stock_name = response.css('.answerBoxOuter .userPic .comName>a::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['stock_name'] = stock_name

        q_time = response.css('.askBoxOuter .msgBox .date::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['q_time'] = q_time

        q_content = response.css('.askBoxOuter .msgBox .msgCnt>div::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['q_content'] = q_content

        a_time = response.css('.answerBoxOuter .answerBox .time .date::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['a_time'] = a_time

        a_content = response.css('.answerBoxOuter .answerBox .msgCnt>a.blue2[target="_blank"]::text').re_first(r'^\s*(\S.+\S)\s*$')
        item['a_content'] = a_content

        yield item
        yield self.request_next()
