# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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
