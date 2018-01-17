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
    sitename = scrapy.Field()
    channel = scrapy.Field()
    url = scrapy.Field()
    groupname = scrapy.Field()
    fund_name = scrapy.Field()
    statistic_date = scrapy.Field()
    nav = scrapy.Field()
    added_nav = scrapy.Field()
    nav_2 = scrapy.Field()
    added_nav_2 = scrapy.Field()
    total_nav = scrapy.Field() #资产净值(元)
    share = scrapy.Field() #资产份额
    income_value_per_ten_thousand = scrapy.Field() #万份收益
    d7_annualized_return = scrapy.Field() #七日年化

