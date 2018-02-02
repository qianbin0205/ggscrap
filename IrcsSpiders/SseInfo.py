# -*- coding: utf-8 -*-

from GGScrapy.items import GGIrcsItem
from GGScrapy.ggspider import GGIrcsSpider


class SseInfoSpider(GGIrcsSpider):
    name = 'Ircs_SseInfo'
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
            item = GGIrcsItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['entry'] = self.entry
            item['url'] = response.url

            asker = record.css('.m_feed_detail.m_qa_detail>.m_feed_face>p::text').re_first(r'^\s*(\S.*\S)\s*$')
            item['asker'] = asker

            stk_code = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_txt>a::text').re_first(
                r':\S+\((\d+)\)')
            item['stk_code'] = stk_code

            stk_name = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_txt>a::text').re_first(
                r':(\S+)\(\d+\)')
            item['stk_name'] = stk_name

            ask_time = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_func>.m_feed_from>span:nth-child(1)::text').re_first(r'^\s*(\S.*\S)\s*$')
            item['ask_time'] = ask_time

            ask_content = record.css('.m_feed_detail.m_qa_detail>.m_feed_cnt>.m_feed_txt').re_first(r'</a>(\S+)\s*</div>')
            item['ask_content'] = ask_content

            reply_time = record.css(
                '.m_feed_detail.m_qa>.m_feed_func>.m_feed_from>span:nth-child(1)::text').re_first(r'^\s*(\S.*\S)\s*$')
            item['reply_time'] = reply_time

            reply_content = record.css('.m_feed_detail.m_qa>.m_feed_cnt>.m_feed_txt::text').re_first(r'^\s*(\S.*\S)\s*$')
            item['reply_content'] = reply_content

            yield item

        self.ips.append({
            'pg': response.meta['pg'] + 1,
            'url': response.meta['url'],
            'ref': response.meta['ref']
        })

        yield self.request_next()
