import re
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class ShanghaidaixiInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShanghaidaixiInvest'
    sitename = '岱熹投资'
    channel = '投资顾问'
    allowed_domains = ['d-shine.cn']

    start_urls = []
    ips = [
        {
            'url': 'http://www.d-shine.cn'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(ShanghaidaixiInvestSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        dateContent = response.xpath('//div[@id="layer26F1634056B183EE12838610E465F39E"]/div/text()').extract_first()
        dateContent = dateContent.split('：')[1]
        statistic_date = dateContent[0:4] + dateContent[5:7] + dateContent[8:10]
        statistic_date = str(statistic_date) if statistic_date is not None else None
        statistic_date = datetime.strptime(statistic_date, '%Y%m%d')

        datas = response.xpath('//div[@id="layer469AE110B41B8B13300182DAC6EEA583"]/div/table/tbody/tr')
        for data in datas[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['statistic_date'] = statistic_date

            item['fund_name'] = data.xpath('./td[1]/text()').extract_first()

            added_nav = data.xpath('./td[4]/text()').extract_first()
            added_nav = re.search(r'([0-9.]+)', str(added_nav))
            added_nav = added_nav.group(0) if added_nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

        yield self.request_next()
