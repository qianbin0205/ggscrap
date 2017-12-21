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
