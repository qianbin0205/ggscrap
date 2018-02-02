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

        pg = int(response.css('.PagesBox .current::text').extract_first())
        if pg < 50:
            form = {}
            for ipt in response.css('#form1 input'):
                name = ipt.css('::attr(name)').extract_first()
                value = ipt.css('::attr(value)').extract_first()
                if name:
                    form[name] = value
            form['pageNo'] = str(pg + 1)

            self.lps.append({
                'url': 'http://irm.cninfo.com.cn/ircs/interaction/lastRepliesForSzse.do',
                'ref': 'http://irm.cninfo.com.cn/ircs/interaction/lastRepliesForSzse.do',
                'form': form
            })

        yield self.request_next()

    def parse_item(self, response):
        item = GGIrcsItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['entry'] = self.entry
        item['url'] = response.url

        # asker = response.css('.askBoxOuter .userPic .userName::text').re_first(r'^\s*(\S.*\S)\s*$')
        asker = response.css('.askBoxOuter .msgBox .msgCnt').xpath(r'.//a[contains(@href,"allQuestionsForQuestioner")]').css('::text').re_first(r'^\s*(\S.*\S)\s*$')
        assert asker is not None
        item['asker'] = asker

        stk_code = response.css('.answerBoxOuter .userPic .comCode>a::text').re_first(r'^\s*(\S.*\S)\s*$')
        item['stk_code'] = stk_code

        stk_name = response.css('.answerBoxOuter .userPic .comName>a::text').re_first(r'^\s*(\S.*\S)\s*$')
        item['stk_name'] = stk_name

        ask_time = response.css('.askBoxOuter .msgBox .date::text').re_first(r'^\s*(\S.*\S)\s*$')
        item['ask_time'] = ask_time

        ask_content = response.css('.askBoxOuter .msgBox .msgCnt>div::text').re_first(r'^\s*(\S.*\S)\s*$')
        item['ask_content'] = ask_content

        reply_time = response.css('.answerBoxOuter .answerBox .time .date::text').re_first(r'^\s*(\S.*\S)\s*$')
        item['reply_time'] = reply_time

        reply_content = response.css('.answerBoxOuter .answerBox .msgCnt').xpath(r'.//a[contains(@href,"allQuestionsForQuestioner")]').xpath(r'following-sibling::text()').re_first(r'^\s*:\s*(\S.*\S)\s*$')
        item['reply_content'] = reply_content

        yield item
        yield self.request_next()
