# -*- coding: utf-8 -*-
import scrapy


class TriethocSpiderSpider(scrapy.Spider):
    name = 'triethoc_spider'
    allowed_domains = ['triethocduongpho.net']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.gen_year()

    def gen_year(self):
        domain = "triethoduongpho.net"
        domains = []
        year_start = 2013
        year_end = 2021
        years = range(2013, 2020, 1)
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
        item = {}
        title = response.xpath('//title/text()').extract_first()
        content = response.xpath(
            "//div[@class='entry-content']/div[1]").extract_first()
        try:
            content = content.split("<hr>")[0]
        except:
            pass

        item["title"] = title
        item["content"] = content
        yield item
