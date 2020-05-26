# -*- coding: utf-8 -*-
import scrapy


class TriethocSpiderSpider(scrapy.Spider):
    name = 'triethoc_spider'
    allowed_domains = ['triethocduongpho.com']
    start_urls = ['http://triethocduongpho.com/']

    def parse(self, response):
        pass
