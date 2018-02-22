import re
import urllib.parse
import json
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url



class UrichInvestSpider(GGFundNavSpider):
    name = 'FundNav_UrichInvest'
    sitename = '佑瑞持'
    channel = '投顾净值'
    allowed_domains = ['urich.cn']
    start_urls = ['http://www.urich.cn/']

    def __init__(self, limit=None, *args, **kwargs):
        super(UrichInvestSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):

            yield Request(url='http://www.urich.cn/Risk.asp?temp=200', callback=self.parse)

    def parse(self, response):

        fps = [
            {
                'url': 'http://www.urich.cn/product.asp',
                'ref':'http://www.urich.cn/Risk.asp?temp=200'
            }
        ]

        yield self.request_next(fps, [])

    def parse_fund(self, response):
        fps = response.meta['fps']
        ips = response.meta['ips']
        ext = response.meta['ext']

        trs = response.xpath("//table[@class='pr_view']/tr")
        for tr in trs[1:]:
            url = tr.xpath("./td[last()]/a/@href").extract_first()
            if url != ''and url is not None:
                if 'http://www.ccbtrust.com.cn/templates/second/index.aspx?nodeid=15&page=ContentPage&' not in url:
                    ips.append({
                        'url': url,
                        'ref': 'http://www.urich.cn/product.asp',
                    })

        yield self.request_next([], ips)

    def parse_item(self, response):
            fps = response.meta['fps']
            ips = response.meta['ips']
            ext = response.meta['ext']
            fund_name = ''
            url = response.url
            if 'https://www.bjitic.com/sun_info-49-52.html' in url:
                   content_name = response.xpath('//div[@class="item"]/div[2]/text()').extract_first()
                   fund_name = content_name.split('：')[1]
                   dataList = response.xpath('//div[@class="qmm_lb"]/table/tr')
                   for data in dataList[1:]:
                        item = GGFundNavItem()
                        item['sitename'] = self.sitename
                        item['channel'] = self.channel
                        item['url'] = response.url

                        item['fund_name'] = fund_name

                        statistic_date = data.xpath('./td[1]/text()').extract_first()
                        statistic_date = str(statistic_date).split(" ")[0] if statistic_date is not None else None
                        statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                        item['statistic_date'] = statistic_date

                        nav = data.xpath('./td[2]/text()').extract_first()
                        nav = re.search(r'([0-9.]+)', str(nav))
                        nav = nav.group(0) if nav is not None else None
                        item['nav'] = float(nav)/10000 if nav is not None else None

                        added_nav = data.xpath('./td[3]/text()').extract_first()
                        added_nav = re.search(r'([0-9.]+)', str(added_nav))
                        added_nav = added_nav.group(0) if added_nav is not None else None
                        item['added_nav'] = float(added_nav)/10000 if added_nav is not None else None

                        yield item

            if 'https://mall.essence.com.cn/mall/views/financial/detail' in url:
                 fund_code = url.rsplit('/',1)[1].split('.')[0]
                 fund_name = response.xpath('//div[@class="lc_b2 reset_lc_b2"]/b/text()').extract_first()
                 url = 'https://mall.essence.com.cn/servlet/json?funcNo=1000055&product_code='+fund_code+'&numPerPage=10&start_date=&end_date=&fund_type=0&page=1'
                 ips.append({
                    'url': url,
                    'ref': 'https://mall.essence.com.cn/mall/views/financial/detail/'+fund_code+'.html',
                    'ext':{'financial':'financial','fund_name':fund_name,'fund_code':fund_code}
                 })

            if 'financial' in ext:
                fund_name = ext['fund_name']
                fund_code = ext['fund_code']
                totalRows =  json.loads(response.text)['results'][0]['totalRows']
                url = 'https://mall.essence.com.cn/servlet/json?funcNo=1000055&product_code=' + str(fund_code) + '&page=1&start_date=&end_date=&fund_type=0&numPerPage=' + str(totalRows)
                ips.append({
                    'url': url,
                    'ref': 'https://mall.essence.com.cn/mall/views/financial/detail/' + str(fund_code) + '.html',
                    'ext': {'financialList': 'financialList', 'fund_name': fund_name, 'fund_code': fund_code}
                })

            if 'financialList' in ext:
                fund_name = ext['fund_name']
                fund_code = ext['fund_code']
                datas = json.loads(response.text)['results'][0]['data']
                for data in datas:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    item['fund_name'] = fund_name

                    statistic_date = data['nav_date']
                    #self.logger.info('statistic_date:'+statistic_date)
                    statistic_date = str(statistic_date).split(" ")[0] if statistic_date is not None else None
                    statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                    item['statistic_date'] = statistic_date

                    nav = data['nav']
                    #self.logger.info('nav:' + nav )
                    nav = re.search(r'([0-9.]+)', str(nav))
                    nav = nav.group(0) if nav is not None else None
                    item['nav'] = float(nav) / 10000 if nav is not None else None

                    added_nav = data['cumulative_net']
                    #self.logger.info('added_nav:' + added_nav)
                    added_nav = re.search(r'([0-9.]+)', str(added_nav))
                    added_nav = added_nav.group(0) if added_nav is not None else None
                    item['added_nav'] = float(added_nav) / 10000 if added_nav is not None else None

                    yield item

            if 'http://www.ciit.com.cn/xingyetrust-web/netvalues/netvalue!getHistoryNetValue' in url:
                url = response.url
                fund_name = url.rsplit('=',1)[1]
                fund_name = urllib.parse.unquote(fund_name)
                fund_url = 'http://www.ciit.com.cn/funds-struts/fund-net-chart-table/XY056X?from=&to=&page=1-16'
                ips.append({
                    'url': fund_url,
                    'ref': 'http://www.ciit.com.cn/xingyetrust-web/netvalues/netvalue!getHistoryNetValue?fundCode=XY056X&fundname=%E5%85%B4%E4%B8%9A%E4%BF%A1%E6%89%98%C2%B7%E4%BD%91%E7%91%9E%E6%8C%81%E4%BC%98%E4%BA%AB%E7%BA%A2%E5%88%A9%E8%AF%81%E5%88%B8%E6%8A%95%E8%B5%84%E9%9B%86%E5%90%88%E8%B5%84%E9%87%91%E4%BF%A1%E6%89%98%E8%AE%A1%E5%88%92',
                    'ext': {'HistoryNetValue': 'HistoryNetValue', 'fund_name': fund_name}
                })

            if 'HistoryNetValue' in ext:
                fund_name = ext['fund_name']
                last_url = response.xpath('//div[@class="dtitle_t"]/table/tr/td[2]/a[last()]/@href').extract_first()
                href = urljoin(get_base_url(response), last_url)
                last_page = href.rsplit('=',1)[1].split('-')[0]
                fund_url = href.rsplit('=',1)[0]
                for page in range(1, int(last_page) + 1):
                    url = fund_url + '=' + str(page) + '-16'
                    ips.append({
                        'url': url,
                        'ref': 'http://www.ciit.com.cn/xingyetrust-web/netvalues/netvalue!getHistoryNetValue?fundCode=XY056X&fundname=%E5%85%B4%E4%B8%9A%E4%BF%A1%E6%89%98%C2%B7%E4%BD%91%E7%91%9E%E6%8C%81%E4%BC%98%E4%BA%AB%E7%BA%A2%E5%88%A9%E8%AF%81%E5%88%B8%E6%8A%95%E8%B5%84%E9%9B%86%E5%90%88%E8%B5%84%E9%87%91%E4%BF%A1%E6%89%98%E8%AE%A1%E5%88%92',
                        'ext': {'HistoryNetValueList': 'HistoryNetValueList', 'fund_name': fund_name}
                    })

            if 'HistoryNetValueList' in ext:
                fund_name = ext['fund_name']
                datas = response.xpath('//table[@class="table2"]/tr')
                for data in datas[1:]:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url

                    item['fund_name'] = fund_name

                    statistic_date = data.xpath('./td[1]/text()').extract_first()
                    statistic_date = str(statistic_date).split(" ")[0] if statistic_date is not None else None
                    statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                    item['statistic_date'] = statistic_date

                    nav = data.xpath('./td[2]/text()').extract_first()
                    nav = re.search(r'([0-9.]+)', str(nav))
                    nav = nav.group(0) if nav is not None else None
                    item['nav'] = float(nav) / 10000 if nav is not None else None

                    yield item

            yield self.request_next(fps, ips)