from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest


class BeiFangxtSpider(GGFundNavSpider):
    name = 'FundNav_BeiFangxt'
    sitename = '北方信托'
    channel = '信托净值'
    allowed_domains = ['www.nitic.cn']
    url = 'http://www.nitic.cn'
    # cookies = '__cfduid=d2771a4ffd6486d083282dc0242a2a37d1518316012; yjs_id=c50471796a2b3c84d5e9f380b5f86582; zjll_productids=138; existFlag=1; vct=9; ctrl_time=1; JSESSIONID=11695FFF42896AA44DFF8E00A6B6BAC6.DLOG4J; Hm_lvt_24b7d5cc1b26f24f256b6869b069278e=1518415092,1518485101; Hm_lpvt_24b7d5cc1b26f24f256b6869b069278e=1518502328; cf_clearance=48d8d72fa1a98401e5b39bec48c5fdc65ee5da7b-1518503327-1800; jiathis_rdc=%7B%22http%3A//www.nitic.cn/news_detail/newsId%3D5893.html%22%3A-1934023915%2C%22http%3A//www.nitic.cn/news_detail/newsId%3D5892.html%22%3A-1918508230%2C%22http%3A//www.nitic.cn/news_list/columnsId%3D58%26%26newsCategoryId%3D8%26FrontNews_list01-002_pageNo%3D2%26FrontNews_list01-002_pageSize%3D20.html%22%3A-1918455585%2C%22http%3A//www.nitic.cn/news_list/columnsId%3D58%26%26newsCategoryId%3D8.html%22%3A-1917113925%2C%22http%3A//www.nitic.cn/news_list/columnsId%3D58%26%26newsCategoryId%3D8%26FrontNews_list01-002_pageNo%3D1%26FrontNews_list01-002_pageSize%3D10.html%22%3A-1915999748%2C%22http%3A//www.nitic.cn/news_detail/newsId%3D5900.html%22%3A0%7C1518503219724%2C%22http%3A//www.nitic.cn/%22%3A%22367%7C1518503252092%22%7D; GUID=6d34d582-484b-4042-bea2-00cc216ae540; pvc=18; BROWSEID=8cf25d8f-e1a4-4d80-8e53-eddf7de49eee; rd=http%3A//www.nitic.cn/'

    def __init__(self, limit=None, *args, **kwargs):
        super(BeiFangxtSpider, self).__init__(limit, *args, **kwargs)

    def start_requests(self):
        yield FormRequest(url='http://www.nitic.cn/news_list/columnsId=58&&newsCategoryId=8.html',
                          headers={'Referer': None,
                                   'Host':'www.nitic.cn',
                                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
                                   },
                      callback=self.parse_page)

    def parse_login(self, response):
        print(response.text)

    def parse_page(self, response):
        # print(response)
        recordInfo = response.css("div.totalcount").xpath("text()").extract()[0]
        recordCounts = recordInfo.split('共')[1].replace(',', '').replace('条', '')
        pageSize = 100
        pageNum = (int(recordCounts)//pageSize)+1
        pageIndex = 1
        while pageIndex <= int(pageNum):
            # print(pageIndex)
            self.fps.append(
                   {
                       'url': 'http://www.nitic.cn/news_list/columnsId=58&&newsCategoryId=8&FrontNews_list01-002_pageNo='+str(pageIndex)+'&FrontNews_list01-002_pageSize='+str(pageSize)+'.html',
                       'ref': response.url,
                       'headers': {
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
                                },
                   }
            )
            pageIndex = pageIndex + 1
        # print(fps)
        yield self.request_next(self.fps)

    def parse_fund(self, response):
        notices = response.css("div.newstitle>ul>li>h3")
        dwNotices = notices.xpath("a[contains(@title,'单位净值')]")
        ips = []
        for notice in dwNotices:
            titile = notice.xpath("@title").extract()[0]
            link = notice.xpath("@href").extract()[0]
            # print(titile)
            if '计划单位净值' in titile:
                continue
            else:
                ips.append(
                            {
                                'url': self.url+link,
                                'ref': response.url,
                                'headers': {
                                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
                                        },
                            }
                    )
        yield self.request_next(self.fps, ips)

    def parse_item(self, response):
        # print(response)
        fundInfo = response.xpath('//div[@id="infoContent"]/table/tbody/tr[2]')
        # print(navInfo)
        for fund in fundInfo:
            try:
                fundName = fund.xpath('td[1]/text()').extract()[0]
                fundNav = fund.xpath('td[2]/text()').extract()[0]
                navDate = fund.xpath('td[3]/text()').extract()[0]

                item = GGFundNavItem()

                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundName.strip('\n').strip('\t')
                init_date = navDate.strip('\n').strip('\t')
                item['statistic_date'] = datetime.strptime(init_date, '%Y-%m-%d')
                nav = fundNav
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = None
                yield item
            except:
                continue
        yield self.request_next()
