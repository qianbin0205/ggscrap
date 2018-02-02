# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider


class JhzqSpider(GGFundNavSpider):
    name = 'FundNav_Jhzq'
    sitename = '江海证券'
    channel = '券商资管净值'
    allowed_domains = ['www.jhzq.com.cn']
    start_urls = ['http://www.jhzq.com.cn/productvalue.jsp']

    def __init__(self, limit=None, *args, **kwargs):
        super(JhzqSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.jhzq.com.cn/productvalue.jsp',
                'ref': None,
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        funds = response.css('#tbData tr>td:first-child a')
        for fund in funds:
            fund_name = fund.xpath('self::a/text()').extract_first()
            pid = fund.css('::attr(href)').re_first(r'id=([^&?]+)')
            ref = urljoin(get_base_url(response), fund.css('::attr(href)').extract_first())
            ips.append({
                'pg': 1,
                'url': 'http://www.jhzq.com.cn/action.jsp',
                'form': {'byAjax': '1', 'pagesize': '100', 'actionType': 'SelectProductjz', 'totalpages': '',
                         'column_id': pid, 'pageNo': lambda pg: str(pg)},
                'ref': ref,
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)

    def parse_item(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        fund_name = ext['fund_name']

        resp = eval(response.text)
        c = int(resp['count'])
        d = resp['dataset']
        for i in range(0, c):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']
            item['fund_name'] = fund_name

            dd = d[str(i)]
            statistic_date = dd['time']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(dd['value'])

            yield item

        totalpages = resp['totalpages']
        form = response.meta['form']
        form['totalpages'] = totalpages

        url = response.meta['url']

        pg = response.meta['pg']
        pages = int(totalpages)
        if pg < pages:
            ips.append({
                'pg': pg + 1,
                'url': url,
                'form': form,
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name}
            })

        yield self.request_next(fps, ips)
