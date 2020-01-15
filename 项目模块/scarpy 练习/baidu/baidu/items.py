# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Join, TakeFirst,Identity


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def dealwith(value):
    value +='2'
    return value


class HuiCItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(dealwith), output_processor=Identity())
    print(title)
