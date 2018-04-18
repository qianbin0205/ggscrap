# coding:utf-8

from datetime import datetime
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class DaoTongFuturesSpider(GGFundNavSpider):
    name = 'FundNav_DaoTongFutures'
    sitename = '道通期货'
    channel = '期货净值'
    allowed_domains = ['www.doto-futures.com']

    def __init__(self, limit=None, *args, **kwargs):
        super(DaoTongFuturesSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        self.ips.append({
            'url': 'http://www.doto-futures.com/zcgl.aspx?CateId=227&Sys_Id=230',
            'ref': 'http://www.longone.com.cn/main/assetmanage/index.html'
        })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = '道通润丰一号'
        tab = response.css('table.MsoNormalTable tr')

        year = 2016
        m2 = '0'
        for row in tab[1:]:
            date = ''.join(row.xpath('td//text()').extract()[:-1]).strip()
            m1 = date.split('月')[0]
            # 抓取没有年份，所以通过1月和12月交替的那两条记录的拼接判断是否跨年
            if m1 + m2 == '121':
                year = year - 1
            statistic_date = str(year) + '年' + date
            nav = row.xpath('td//text()').extract()[-1]
            m2 = m1

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
            item['nav'] = float(nav)

            yield item

        yield self.request_next()
