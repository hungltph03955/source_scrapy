# -*- coding: utf-8 -*-
import scrapy

from ..items import SourceTrietHocItem


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
        next_page = response.xpath(
            "//div[@class='pagination']/a/text()").extract()
        total_page = int(next_page[-1])
        list_page = self.gen_page(total_page, response.url)

        for item_page in list_page:
            yield scrapy.Request(item_page, self.parse_list)

    def parse_list(self, response):
        list_la = response.xpath('//article/header/h2/a/@href').extract()
        for list_la_item in list_la:
            yield scrapy.Request(list_la_item, self.parse_detail)

    def parse_detail(self, response):
        item = SourceTrietHocItem()

        title = response.xpath('//title/text()').extract_first()
        content = response.xpath(
            "//div[@class='entry-content']/div[1]").extract_first()
        try:
            content = content.split("<hr>")[0]
        except:
            pass

        item["title"] = title
        item["content"] = content
        item["image_urls"] = response.xpath(
            '//div[@class="entry-featured"]/img/@src'
        ).extract()
        yield item
