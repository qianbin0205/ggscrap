from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class EstockSpider(GGFundNavSpider):
    name = 'FundNav_Estock'
    sitename = '大通证券'
    channel = '券商资管净值'
    allowed_domains = ['www.estock.com.cn']
    start_urls = ['http://www.estock.com.cn/?q=dt_panel_cpzx']

    def __init__(self, *args, **kwargs):
        super(EstockSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fps = [
            {
                'url': 'http://www.estock.com.cn/?q=dt_panel_cpzx'
            }
        ]
        yield self.request_next(fps, [])

    def parse_fund(self, response):

        fund_link = response.xpath('//div[@class="pane-content"]//p//input//@onclick').extract()

        for n in fund_link[2:5]:
            key = n.replace('window.open(\'', '').replace('/\')', '')
            link_key = 'http://www.estock.com.cn' + key + '&page=' + '0'
            self.ips.append({
                'url': link_key,
                'pg': 0
            })
        yield self.request_next()

    def parse_item(self, response):
        rows = response.xpath('//tbody//tr')

        if rows:

            for row in rows:
                row_info = row.xpath('td/text()').extract()
                if '%' in row_info[4].strip():
                    continue
                else:
                    fund_name = row_info[1].strip()
                    statistic_date = row.xpath('td//span/text()').extract_first()
                    nav = row_info[4].strip()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
                item['nav'] = float(nav) if nav is not None else None

                yield item

            page = response.meta['pg']
            next_pg = int(page) + 1
            url = response.url.replace('&page=' + str(page), '&page=' + str(next_pg))
            self.ips.append({
                'url': url,
                'ref': response.url,
                'pg': next_pg,
            })

        yield self.request_next()
