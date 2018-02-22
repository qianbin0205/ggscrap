# -*- coding: utf-8 -*-
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class MaodianSpider(GGFundNoticeSpider):
    name = 'FundNotice_Maodian'
    sitename = '茂典资产'
    channel = '公告'
    entry = 'http://www.md-amc.com'
    allowed_domains = ['www.md-amc.com']
    start_urls = []

    lps = [
        {
            'url': 'http://www.md-amc.com/info.asp?second_id=2002',
            'ref': 'http://www.md-amc.com/'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(MaodianSpider, self).__init__(*args, **kwargs)

    def parse_list(self, response):
        ext = response.meta['ext']

        if 'type' not in ext:
            page_end_href = response.xpath('//div[@class="page_no"]/a[@class="page_end"]/@href').extract_first()
            page_end = page_end_href.rsplit('=',1)[1]
            page_href = page_end_href.rsplit('=',1)[0]

            for page in range(1,int(page_end)+1):
                url = page_href+"="+str(page)
                url= urljoin(get_base_url(response), url)
                self.lps.append({
                    'url': url,
                    'headers': {'Content-Type': 'application/json;charset=UTF-8'},
                    'ref': response.url,
                    'ext': {'type': '1'}
                })
        else:
            rows = response.xpath('//div[@class="list_news_01"]/ul/li')
            for row in rows:
                row_href = row.xpath('./a/@href').extract_first()
                url = urljoin(get_base_url(response), row_href)
                self.ips.append({
                    'url': url,
                    'headers': {'Content-Type': 'application/json;charset=UTF-8'},
                    'ref': response.url,
                })

        yield self.request_next()

    def parse_item(self, response):
        title = response.xpath('//div[@class="display_title"]/h1/text()').extract_first()
        info = response.xpath('//div[@class="display_title"]/div[@class="info"]').extract_first()
        info = info.rsplit("</span>",1)[1]
        info = info.rsplit("浏览次数",1)[0]
        info = info.strip().replace("\n", "").replace("\r", "").replace("\t", "")
        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['url'] = response.url
        item['title'] = title
        publish_time = info
        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
        yield item

        yield self.request_next()
