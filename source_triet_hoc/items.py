# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
import re


def filer_content(content):
    try:
        content = content.replace("<br>", "</p>\n<p>")
    except:
        pass

    try:
        content = re.sub("<a.*?>(.+?)</a>", "", content)
    except:
        pass
    try:
        content = re.sub("<strong.*?>(.+?)</strong>", "", content)
    except:
        pass
    try:
        content = re.sub("<p.*?>(.+?)</strong></p>", "", content)
    except:
        pass
    return content


class SourceTrietHocItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst(),
    )
    content = scrapy.Field(
        input_processor=MapCompose(filer_content),
        output_processor=Join(),
    )
    image_urls = scrapy.Field() # default
    images = scrapy.Field() # default
