# -*- coding: utf-8 -*-

from GGScrapy.items import GGInteractionItem
from GGScrapy.ggspider import GGInteractionSpider


class SseInfoSpider(GGInteractionSpider):
    name = 'Interaction_SseInfo'
    sitename = '上证e互动'
    channel = '投资者关系互动平台-最新回复'
    entry = 'http://sns.sseinfo.com/qa.do'
    allowed_domains = ['sns.sseinfo.com']

    start_urls = []
    ips = [
        {
            'pg': 1,
            'url': lambda pg: 'http://sns.sseinfo.com/ajax/feeds.do?page=' + str(
                pg) + '&type=11&pageSize=10&lastid=-1&show=1',
            'ref': 'http://sns.sseinfo.com/qa.do'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(SseInfoSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        records = response.css('.m_feed_item')
        for record in records:
            item = GGInteractionItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            author = record.css('.m_feed_detail.m_qa_detail>.m_feed_face>p::text').extract_first()
            item['author'] = author

            stock_code = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_txt>a::text').re_first(
                r':\S+\((\d+)\)')
            item['stock_code'] = stock_code

            stock_name = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_txt>a::text').re_first(
                r':(\S+)\(\d+\)')
            item['stock_name'] = stock_name

            q_time = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_func>.m_feed_from>span:nth-child(1)::text').extract_first()
            item['q_time'] = q_time

            q_content = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_txt').re_first(r'</a>(\S+)\s*</div>')
            item['q_content'] = q_content

            a_time = record.css(
                '.m_feed_detail.m_qa>.m_feed_func>.m_feed_from>span:nth-child(1)::text').extract_first()
            item['a_time'] = a_time

            a_content = record.css('.m_feed_detail.m_qa>.m_feed_cnt>.m_feed_txt::text').extract_first()
            if a_content:
                a_content = a_content.strip()
            item['a_content'] = a_content

            yield item

        self.ips.append({
            'pg': response.meta['pg'] + 1,
            'url': response.meta['url'],
            'ref': response.meta['ref']
        })

        yield self.request_next()
