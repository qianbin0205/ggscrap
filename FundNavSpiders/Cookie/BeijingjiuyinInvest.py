import re
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class BeijingjiuyinInvestSpider(GGFundNavSpider):
    name = 'FundNav_BeijingjiuyinInvest'
    sitename = '北京久银投资'
    channel = '投资顾问'
    allowed_domains = ['eagle-fund.com']

    username = '13523794375'
    password = '12345'
    cookies = 'hVyFVN_think_language=zh-CN; PHPSESSID=ui2p5dcpkd70reagvea4pqduv7'

    start_urls = []
    fps = [
        {
            'url': 'http://www.eagle-fund.com/index.php?m=list&a=index&id=24',
            'ref': 'http://www.eagle-fund.com/index.php?g=portal&m=list&a=index&id=6'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(BeijingjiuyinInvestSpider, self).__init__(*args, **kwargs)

    def parse_fund(self, response):
        datas = response.xpath('//ul[@class="mid_ul_span"]/table/tbody/tr')
        for data in datas[1:]:
            href = data.xpath('./td[1]/p/a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            self.ips.append({
                'url': url,
                'ref': response.url,
            })

        yield self.request_next()

    def parse_item(self, response):
        datas = response.xpath('//table[@class="table table-bordered"]/tbody/tr')
        for data in datas:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = data.xpath('./td[1]/text()').extract_first()

            statistic_date = data.xpath('./td[2]/text()').extract_first()
            statistic_date = str(statistic_date) if statistic_date is not None else None
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['statistic_date'] = statistic_date

            nav = data.xpath('./td[3]/text()').extract_first()
            nav = re.search(r'([0-9.]+)', str(nav))
            nav = nav.group(0) if nav is not None else None
            item['nav'] = float(nav) if nav is not None else None

            yield item

        yield self.request_next()
