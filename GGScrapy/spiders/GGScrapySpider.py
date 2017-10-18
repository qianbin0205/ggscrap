# -*- coding: utf-8 -*-
import scrapy


class GGScrapySpider(scrapy.Spider):
    name = 'GGScrapySpider'
    allowed_domains = ['www.go-goal.com']
    start_urls = ['http://www.go-goal.com/']

    def parse(self, response):
        pass
