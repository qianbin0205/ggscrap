# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-16

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import json


class GuangFaAssetSpider(GGFundNavSpider):
    name = 'FundNav_GuangFaAsset'
    sitename = '广发证券'
    channel = '券商资管净值'
    username = '522101197011052410'
    password = 'ZYYXSM123'
    cookies = 'GF_STORE_TRACK=5ad7314da41e863f5e010d9a; gfportalsid=s%3A5f8fc1a0-5907-11e8-ad30-ed70880fec7d_24114_432954_21.gU2udrU8k8tfeOACJIgyj1SsOC2K6NJX6pEmqf6HKac; gfwebsid=eyJ1c2VyIjp7ImN1c3RuYW1lIjoiWllZWFNNIiwiY3VzdG5vIjoiMTM5MTY0Mjc5MDYiLCJjdXN0bm9MaXN0IjpbIjEzOTE2NDI3OTA2Il0sInBob25lIjoiMTM5MTY0Mjc5MDYiLCJiYXVnaHRQcm9kQ29kZUxpc3QiOltdLCJmdW5kQWNjb3MiOltdLCJpZGVudGl0eW5vIjoiNTIyMTAxMTk3MDExMDUyNDEwIiwiaWRlbnRpdHlUeXBlIjoiMSIsInBhc3N3b3JkIjpudWxsLCJnemNvZGUiOm51bGwsImNsaWVudElkIjpudWxsLCJwZXJpb2RUeXBlIjoiNCIsImludmVzdFR5cGUiOiI1Iiwicmlza0xldmVsIjoiNSIsInVzZXJDYXRlZ29yeSI6IjEiLCJ1c2VyVHlwZSI6MSwic2lnbklkIjpudWxsLCJ1c2VyX3R5cGUiOiIxIn19; gfwebsid.sig=Op9-uIc-O5ejIUCKNSKqRU47NzI'
    # fps = [{'url': 'https://www.gfam.com.cn/product/search_index'}]
    fps = [{
        'url': 'https://www.gfam.com.cn/product/list?page=1&pageSize=200',
        'pg': 1
    }]

    def parse_fund(self, response):
        fund_rows = response.css('tbody tr')
        if fund_rows:
            for r in fund_rows:
                pcode = r.css('td:nth-child(2)::text').extract_first()
                pname = r.css('td:nth-child(3) a::text').extract_first()
                # ptype = r.css('td:nth-child(4)::text').extract_first(default='none_type').strip()

                self.ips.append({
                    'url': 'https://www.gfam.com.cn/product/detail/%s' % pcode,
                    'ref': response.url,
                    'pg': 1,
                    'ext': {
                        'pname': pname,
                        # 'ptype': ptype
                    }
                })

            next_pg = response.meta['pg'] + 1
            self.fps.append({
                'url': 'https://www.gfam.com.cn/product/list?page=%s&pageSize=200' % next_pg,
                'pg': next_pg
            })

    def parse_item(self, response):
        if 'product/detail' in response.url:
            # 接收第一次PRASE_FUND传过来的URL，主要是用来解析标签
            # 集合净值
            jhjz_href = response.xpath(
                '//tr[@class="info_hd"]//a[contains(@onclick, "cpzx_jhlc_jhjz")]/@onclick').re_first("'(.*)'")
            if jhjz_href:
                pg = 1
                href = jhjz_href + '&page=%s&pageSize=200' % pg
                self.ips.append({
                    'url': 'https://www.gfam.com.cn%s' % href,
                    'ref': response.url,
                    'pg': pg
                })

            # 份额收益
            fesy_href = response.xpath(
                '//tr[@class="info_hd"]//a[contains(@onclick, "cpzx_jhlc_fesy")]/@onclick').re_first("\?(.*)'\)")
            if fesy_href:
                pg = 1
                href = fesy_href + '&page=%s&pageSize=200' % pg
                self.ips.append({
                    'url': 'https://www.gfam.com.cn/product/portionProfit?%s' % href,
                    'ref': response.url,
                    'pg': pg
                })

        # ------------------------------------------------------
        # 解析第一次分类后的详细RESPONSE
        # 集合净值
        if 'cpzx_jhlc_jhjz' in response.url:
            rows = response.css('tbody tr')
            if rows:
                next_pg = response.meta['pg'] + 1
                self.ips.append({
                    'url': re.sub('page=\d+', 'page=' + str(next_pg), response.url),
                    'ref': response.url,
                    'pg': next_pg
                })

                # 表头都是动态的，索引净值位置再解析入库
                tb_hearer = response.css('thead th::text').extract()
                for r in rows:
                    date_index = tb_hearer.index('日期')
                    dt_path = 'td:nth-child(%s)::text' % (date_index + 1)
                    date = r.css(dt_path).extract_first()

                    nav_index = tb_hearer.index('单位净值')
                    nav = None
                    if nav_index:
                        nav_path = 'td:nth-child(%s)::text' % (nav_index + 1)
                        nav = r.css(nav_path).extract_first()

                    add_nav_index = tb_hearer.index('累计净值')
                    add_nav = None
                    if add_nav_index:
                        add_nav_path = 'td:nth-child(%s)::text' % (add_nav_index + 1)
                        add_nav = r.css(add_nav_path).extract_first()

                    f_name_index = tb_hearer.index('份额名称')
                    f_name = response.meta['ext']['fund_name']
                    if f_name_index:
                        f_name_path = 'td:nth-child(%s)::text' % (f_name_index + 1)
                        f_name = r.css(f_name_path).extract_first()

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = f_name
                    item['statistic_date'] = date
                    item['nav'] = float(nav) if nav else None
                    item['added_nav'] = float(add_nav) if add_nav else None

                    yield item

        # 份额收益
        if 'cpzx_jhlc_fesy' in response.url:
            rows = response.css('tbody tr')
            if rows:
                next_pg = response.meta['pg'] + 1
                self.ips.append({
                    'url': re.sub('page=\d+', 'page=' + str(next_pg), response.url),
                    'ref': response.url,
                    'pg': next_pg
                })

                for r in rows:
                    date = r.css('td:nth-child(1)::text').extract_first()
                    tt_inc = r.css('td:nth-child(2)::text').extract_first()
                    d7 = r.css('td:nth-child(3)::text').extract_first()
                    f_name = response.meta['ext']['fund_name']

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = f_name
                    item['statistic_date'] = date
                    item['income_value_per_ten_thousand'] = float(tt_inc) if tt_inc else None
                    item['d7_annualized_return = Field'] = float(d7) if d7 else None

                    yield item

            # 下面误删可能还有用

            # # 份额单位净值
            # fedwjz_href = response.xpath(
            #     '//tr[@class="info_hd"]//a[contains(@onclick, "cpzx_jhlc_fedwjz")]/@onclick').re_first("\?(.*)'\)")
            # if fedwjz_href:
            #     self.ips.append({
            #         'url': 'https://www.gfam.com.cn/product/unitnetsHightChart?%s' % fedwjz_href,
            #         'ref': response.url
            #     })

            # # 业绩基准
            # yqsy_href = response.xpath(
            #     '//tr[@class="info_hd"]//a[contains(@onclick, "cpzx_jhlc_yqsy")]/@onclick').re_first("\?(.*)'\)")
            # if yqsy_href:
            #     self.ips.append({
            #         'url':
            #
            #     })
