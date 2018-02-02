import re
from scrapy import Request
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class InforeCapitalSpider(GGFundNavSpider):
    name = 'FundNav_InforeCapital'
    sitename = '盈峰资本'
    channel = '投顾净值'
    allowed_domains = ['inforecapital.com']

    username = '15838535216'
    password = '050835'
    cookies = 'zh_choose=n; UM_distinctid=1614fff05b7430-0c1b13b0fb8555-6f16107f-1fa400-1614fff05b8932; 7731da3e46531bacd3fffe42cdd43967=104; PHPSESSID=0gmgmhgfd5da8492rkl2q2qcd7; CNZZDATA1261971137=68816170-1517465804-%7C1517548645'

    start_urls = []
    fps = [
        {
            'url': 'http://www.inforecapital.com/Product_index.html',
            'ref': 'http://www.inforecapital.com/Users_index.html'
        }
    ]

    def __init__(self, limit=None, *args, **kwargs):
        super(InforeCapitalSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield Request(url='http://www.inforecapital.com/Index_index.html', callback=self.parse_login)

    def parse_login(self, response):
        yield self.request_next()

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']

        current_page = response.xpath('//div[@class="page"]/div/span/text()').extract_first()
        next_url = response.xpath('//div[@class="page"]/div/a[@class="next"]/@href').extract_first()
        if next_url is not None:
            next_page = next_url.split('.')[0].rsplit('_',1)[1]
            if int(next_page) > int(current_page):
                next_url = urljoin(get_base_url(response), next_url)
                fps.append({
                        'url': next_url,
                        'ref': response.url,
                    })

        lis = response.xpath('//div[@class="container_1"]/ul/li')
        for li in lis:
            href = li.xpath('./a/@href').extract_first()
            fund_name = li.xpath('./a/h3/text()').extract_first()
            if 'p_' in href:
                fund_code = href.rsplit('/', 1)[1].rsplit('_', 4)[0]
            else:
              fund_code = href.rsplit('/',1)[1].rsplit('_',2)[0]
            #self.logger.info('http://www.inforecapital.com/'+fund_code+'_type_unit.html')
            ips.append({
                'url': 'http://www.inforecapital.com/'+fund_code+'_type_unit.html',
                'ref': response.url,
                'ext':{'fund_name':fund_name}
            })


        yield self.request_next(fps, ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']
            ext = response.meta['ext']
            fund_name = ext['fund_name']

            current_page = response.xpath('//div[@class="page"]/div/span/text()').extract_first()
            next_url = response.xpath('//div[@class="page"]/div/a[@class="next"]/@href').extract_first()
            if next_url is not None:
                next_page = next_url.split('.')[0].rsplit('_', 1)[1]
                if next_page =='unit':
                    next_page = next_url.split('.')[0].rsplit('_', 3)[1]
                if int(next_page) > int(current_page):
                    next_url = urljoin(get_base_url(response), next_url)
                    ips.append({
                        'url': next_url,
                        'ref': response.url,
                        'ext': {'fund_name': fund_name, 'pages': 'true'}
                    })

            datas = response.xpath('//table[@class="tab_pro t_c"]/tr')
            for data in datas[1:]:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name

                statistic_date = data.xpath('./td[1]/text()').extract_first()
                statistic_date = str(statistic_date) if statistic_date is not None else None
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['statistic_date'] = statistic_date

                nav = data.xpath('./td[2]/text()').extract_first()
                nav = re.search(r'([0-9.]+)', str(nav))
                nav = nav.group(0) if nav is not None else None
                item['nav'] = float(nav) if nav is not None else None

                added_nav = data.xpath('./td[3]/text()').extract_first()
                added_nav = re.search(r'([0-9.]+)', str(added_nav))
                added_nav = added_nav.group(0) if added_nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item

            yield self.request_next(fps, ips)