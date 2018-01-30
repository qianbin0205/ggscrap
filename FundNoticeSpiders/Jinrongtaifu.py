# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNoticeItem
from GGScrapy.ggspider import GGFundNoticeSpider


class JinrongtaifuSpider(GGFundNoticeSpider):
    name = 'FundNotice_Jinrongtaifu'
    sitename = '北京锦融泰富投资'
    allowed_domains = ['www.jinrongtaifu.com']
    start_urls = []

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'PHPSESSID=i2rpf84atqpttkdsjt6h6vq1l6; PHPSESSID_NS_Sig=oenCV6mfwDxivAm8; td_cookie=11049137'

    lps = [
        {
            'ch': {
                'name': '产品中心-产品报告',
                'url_entry': 'http://www.jinrongtaifu.com/?Index/View&i=3',
                'count': 0
            },
            'url': 'http://www.jinrongtaifu.com/?Index/View&i=3',
            'ref': 'http://www.jinrongtaifu.com/?Index/Index'
        },
        {
            'ch': {
                'name': '投研中心-公司动态',
                'url_entry': 'http://www.jinrongtaifu.com/?Index/View&i=20',
                'count': 0
            },
            'url': 'http://www.jinrongtaifu.com/?Index/View&i=20',
            'ref': 'http://www.jinrongtaifu.com/?Index/Index'
        },
        {
            'ch': {
                'name': '投研中心-产品公告',
                'url_entry': 'http://www.jinrongtaifu.com/?Index/View&i=24',
                'count': 0
            },
            'url': 'http://www.jinrongtaifu.com/?Index/View&i=24',
            'ref': 'http://www.jinrongtaifu.com/?Index/Index'
        },
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(JinrongtaifuSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield self.request_next()

    def parse_list(self, response):
        pi = response.meta['pi']
        ch = pi['ch']
        if response.url == 'http://www.jinrongtaifu.com/?Index/View&i=3':
            funds = response.xpath("//div[@class='fund-list m-t-20 m-b-40']/table/tr/td[1]/a")
            for fund in funds:
                url = fund.xpath("./@href").extract_first()
                url = urljoin(get_base_url(response), url)
                self.ips.append({
                    'ch': ch,
                    'url': url,
                    'ref': response.url,

                })
        else:
            funds = response.xpath("//div[@class='tab-cont m-t-10 m-b-40']/ul/li")
            for fund in funds:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = ch['name']
                item['url_entry'] = ch['url_entry']
                url = fund.xpath("./a[1]/@href").extract_first()
                item['url'] = urljoin(get_base_url(response), url)
                item['title'] = fund.xpath("./a[1]/text()").extract_first()
                publish_time = fund.xpath("./a[2]/text()").extract_first()
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                yield item
        yield self.request_next()

    def parse_item(self, response):
        pi = response.meta['pi']
        ch = pi['ch']
        funds = response.xpath("//div[@class='item clearfix']")
        for fund in funds:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = ch['name']
            item['url_entry'] = ch['url_entry']
            url = fund.xpath(".//div[@class='caozuo']/a/@href").extract_first()
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = fund.xpath("./div[@class='pdf-title']/text()").extract_first()

            publish_time = fund.xpath(".//div[@class='caozuo']/a/@href").re_first(r'/upload/jinrongtaifu(\d+)\.pdf')[0:8]
            item['publish_time'] = datetime.strptime(publish_time, '%Y%m%d')
            yield item
            ch['count'] = ch['count'] + 1
        yield self.request_next()

