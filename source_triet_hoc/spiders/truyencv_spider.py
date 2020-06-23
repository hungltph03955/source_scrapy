# -*- coding: utf-8 -*-
import scrapy

from ..items import SourceTrietHocItem
from scrapy.loader import ItemLoader


class XpathControler(object):
    categories = '//div[@class="navbar-category"][2]/ul/li/a/@href'
    total_page = '//ul[@class="pull-right pagination"]/li[last()]/a/@href'
    link_story_detail = '//div[@class="block block-default"]/div[@class="block-content"]/ul[@class="list-group"]/li/div/a/@href'


xpath_ctl = XpathControler()


def gen_link_page_story(url, total_page):
    list_page = []
    category_name = url.split("/")[-2]
    for i in range(1, total_page + 1):
        category_link = f"https://truyencv.com/{category_name}/trang-{i}/"
        list_page.append(category_link)

    return list_page


class TruyencvSpider(scrapy.Spider):
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
        "IMAGES_STORE": "download/truyencv/media/image/"

    }
    name = 'truyencv_spider'
    allowed_domains = ['truyencv.com', 'nuhiep.com']
    start_urls = ['https://truyencv.com/']

    def parse(self, response):
        categories = response.xpath(xpath_ctl.categories).extract()
        for category in categories:
            yield scrapy.Request(category, self.category_detail)

    def category_detail(self, response):
        total_page = response.xpath(xpath_ctl.total_page).extract_first()
        total_page = int(total_page.split('-')[-1].replace("/", ""))
        list_page = gen_link_page_story(response.url, total_page)

        for link_item in list_page:
            yield scrapy.Request(link_item, self.story_list)

    def story_list(self, response):
        link_story_detail = response.xpath(
            xpath_ctl.link_story_detail).extract()

        for link_item in link_story_detail:
            yield scrapy.Request(link_item, self.story_detail)

    def story_detail(self, response):

        # def gen_year(self):
        #     domain = "triethocduongpho.net"
        #     domains = []
        #     year_start = 2020
        #     year_end = 2021
        #     years = range(year_start, year_end, 1)
        #     for year in years:
        #         domains.append(f"{domain}/{year}/")

        #     return domains

        # def start_requests(self):
        #     for url in self.start_urls:

        #         yield scrapy.Request(f'https://{url}', self.parse)

        # def gen_page(self, total_page, response_current):
        #     list_page = []
        #     for page in range(1, total_page + 1, 1):
        #         list_page.append(f"{response_current}/page/{page}")

        #     return list_page

        # def parse(self, response):
        #     next_page = response.xpath(xpath_ctl.next_page).extract()
        #     total_page = int(next_page[-1])
        #     list_page = self.gen_page(total_page, response.url)

        #     for item_page in list_page:
        #         yield scrapy.Request(item_page, self.parse_list)

        # def parse_list(self, response):
        #     list_la = response.xpath(xpath_ctl.list_la).extract()
        #     for list_la_item in list_la:
        #         yield scrapy.Request(list_la_item, self.parse_detail)

        # def parse_detail(self, response):
        #     il = ItemLoader(item=SourceTrietHocItem(), response=response)
        #     il.add_xpath('title', xpath_ctl.title)
        #     il.add_xpath('content', xpath_ctl.content)
        #     il.add_xpath('image_urls', xpath_ctl.image_urls)
        #     return il.load_item()
