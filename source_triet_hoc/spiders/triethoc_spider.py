# -*- coding: utf-8 -*-
import scrapy

from ..items import SourceTrietHocItem
from scrapy.loader import ItemLoader

class XpathControler(object):
    title = '//title/text()'
    content = "//div[@class='entry-content']/div[1]/p"
    image_urls = '//div[@class="entry-featured"]/img/@src'
    next_page = "//div[@class='pagination']/a/text()"
    list_la = '//article/header/h2/a/@href'


xpath_ctl = XpathControler()

class TriethocSpiderSpider(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        'CONCURRENT_REQUESTS': 1,
        "FILES_STORE": "download/file/",
        "SPIDER_MIDDLEWARES": {
            'source_triet_hoc.middlewares.SourceTrietHocSpiderMiddleware': 543,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'source_triet_hoc.middlewares.SourceTrietHocDownloaderMiddleware': 543,
        },
        "IMAGES_STORE": "download/media/image/"

    }
    name = 'triethoc_spider'
    allowed_domains = ['triethocduongpho.net']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.gen_year()

    def gen_year(self):
        domain = "triethocduongpho.net"
        domains = []
        year_start = 2020
        year_end = 2021
        years = range(year_start, year_end, 1)
        for year in years:
            domains.append(f"{domain}/{year}/")

        return domains

    def start_requests(self):
        for url in self.start_urls:

            yield scrapy.Request(f'https://{url}', self.parse)

    def gen_page(self, total_page, response_current):
        list_page = []
        for page in range(1, total_page + 1, 1):
            list_page.append(f"{response_current}/page/{page}")

        return list_page

    def parse(self, response):
        next_page = response.xpath(xpath_ctl.next_page).extract()
        total_page = int(next_page[-1])
        list_page = self.gen_page(total_page, response.url)

        for item_page in list_page:
            yield scrapy.Request(item_page, self.parse_list)

    def parse_list(self, response):
        list_la = response.xpath(xpath_ctl.list_la).extract()
        for list_la_item in list_la:
            yield scrapy.Request(list_la_item, self.parse_detail)

    def parse_detail(self, response):
        il = ItemLoader(item=SourceTrietHocItem(), response=response)
        il.add_xpath('title', xpath_ctl.title)
        il.add_xpath('content', xpath_ctl.content)
        il.add_xpath('image_urls', xpath_ctl.image_urls)
        return il.load_item()
