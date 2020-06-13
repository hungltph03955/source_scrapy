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
        content = re.sub("<strong.*?>(.+?)</strong>", "", content)
    except:
        pass
    try:
        content = re.sub("<p.*?>(.+?)</strong></p>", "", content)
    except:
        pass
    content = content.replace("<br>", "</p>\n<p>")
    content = re.sub("<a.*?>(.+?)</a>", "", content)
    content = re.sub("<p><script.*?(.+?)</script>", "", content)
    cont = re.match("<p><img(.+?)</p>", content)
    if cont is not None:
        a = f"<figure><img {cont.group(1)} </figure>"
        content = content.replace(cont.group(0), a)
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
