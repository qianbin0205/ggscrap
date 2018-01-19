from datetime import datetime
from GGScrapy.items import GGFundNavItem
from GGScrapy.ggspider import GGFundNavSpider
from scrapy import Request
from scrapy.utils.response import  get_base_url
from urllib.parse import  urljoin

class ZhejiangBakexiaInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZhejiangBakexiaInvest'
    sitename = '浙江巴克夏投资'
    channel = '投资顾问'
    allowed_domains = ['bkxtz.com']
    start_urls = ['http://www.bkxtz.com/ajax_asp/newsdll_list.asp?menuid=35&sortid=0']
    #itemList = []
    def get_next_url(self, oldUrl, lastPage):
        nextpage = 1
        nextUlr = oldUrl
        if("page" in oldUrl):
            temp = oldUrl.split("&")
            nowPage = temp[1].split("=")[1]
            if(int(nowPage) < lastPage):
                nextPage = int(nowPage)+1
            else:
                nextPage = lastPage
            nextUlr =temp[0]+"&page="+str(nextPage)+"&"+temp[2]
        else :
            nextPage = 2
            nextUrl = oldUrl+"&page="+str(nextPage)
        return nextUrl

    def parse_fund(self, response):
        fundList = response.xpath("//div[@class='remark']/table/tbody/tr")
        if len(fundList) !=0:
            for fund in fundList:
                fundTr = fund.extract()
                if("firstRow" in fundTr):
                    continue
                size = len(fund.xpath("./td"))
                item = []
                for index in range(1,size+1):
                    if index == 2:
                        fundName = []
                        fundNameSpans = fund.xpath("./td["+str(index)+"]/p/strong")
                        if len(fundNameSpans) == 0:
                            fundNameSpans = fund.xpath("./td["+str(index)+"]/p")
                        if len(fundNameSpans) != 0:
                            for fundNameSpan in fundNameSpans:
                                num = len(fundNameSpan.xpath("./span"))
                                for i in range(1, num+1):
                                    spanText = fundNameSpan.xpath("./span["+str(i)+"]/text()").extract()
                                    fundName.append(spanText[0])
                                    if len(fundNameSpan.xpath("./span["+str(i)+"]/span")) != 0:
                                        spanSize = len(fundNameSpan.xpath("./span["+str(i)+"]/span"))
                                        for j in range(1, spanSize+1):
                                            spanText = fundNameSpan.xpath("./span["+str(i)+"]/span["+str(j)+"]/text()").extract()
                                            fundName.append(spanText[0])

                        text = "".join(fundName)
                        if len(text) != 0:
                         item.append(text)
                    else :
                        text = fund.xpath("./td["+str(index)+"]/p/strong/span/text()").extract()
                        if len(text) == 0:
                            text = fund.xpath("./td[" + str(index) + "]/p/span/text()").extract()
                        if len(text) != 0:
                         item.append(text[0])
                navItem = GGFundNavItem()
                navItem['sitename'] = self.sitename
                navItem['channel'] = self.channel
                navItem['url'] = response.request.headers['Referer']
                navItem['fund_name'] = item[1]
                navItem['nav'] = float(item[2]) if item[2] is not None else None
                navItem['added_nav_2'] = float(item[3]) if item[3] is not None else None
                navItem['statistic_date'] = datetime.strptime(item[4], '%Y-%m-%d')
                yield navItem
                #self.itemList.append(navItem)
                #self.logger.info("内容：%s,%s，%s，%s,%s，%s，%s",  navItem['fund_name'], navItem['nav'], navItem['added_nav_2'], navItem['statistic_date'], navItem['sitename'], navItem['channel'], navItem['url'])


    def parse(self, response):
        url = response.url
        lastUrl = response.xpath("//div/ul/li[last()]/a/@href").extract()
        ppList = response.xpath("//ul[@class='pp_n_list']/li/a/@href").extract()
        for pp in ppList:
            ppUrl =  urljoin(get_base_url(response), pp)
            yield Request(ppUrl, callback=self.parse_fund)
        if len(lastUrl) != 0:
          lastPage = lastUrl[0].split("=")[2]
          nextUrl = self.get_next_url(url, int(lastPage))
          if nextUrl:
           yield Request(nextUrl, callback=self.parse)
