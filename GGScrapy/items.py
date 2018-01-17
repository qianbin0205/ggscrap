# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 新闻资讯Item
class GGNewsItem(scrapy.Item):
    sitename = scrapy.Field()
    channel = scrapy.Field()
    url = scrapy.Field()
    groupname = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    pubtime = scrapy.Field()
    content = scrapy.Field()


# 基金净值Item
class GGFundNavItem(scrapy.Item):
    sitename = scrapy.Field()                       # 站点名称
    channel = scrapy.Field()                        # 频道名称
    groupname = scrapy.Field()                      # 分组名称
    fund_name = scrapy.Field()                      # 基金名称
    statistic_date = scrapy.Field()                 # 统计日期
    fund_code = scrapy.Field()                      # 基金代码
    url = scrapy.Field()                            # 链接地址
    nav = scrapy.Field()                            # 单位净值(单位: 元)
    added_nav = scrapy.Field()                      # 累计净值(单位: 元)
    nav_2 = scrapy.Field()                          # 含业绩报酬的单位净值(单位: 元)
    added_nav_2 = scrapy.Field()                    # 含业绩报酬的累计单位净值(单位: 元)
    total_nav = scrapy.Field()                      # 总资产净值(单位: 元)
    share = scrapy.Field()                          # 资产份额(单位: 份)
    income_value_per_ten_thousand = scrapy.Field()  # 每万份计划收益(单位: 元)
    d7_annualized_return = scrapy.Field()           # 7日年化收益率(单位: %)

