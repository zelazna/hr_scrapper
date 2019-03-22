# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HrItem(scrapy.Item):
    date = scrapy.Field()
    text = scrapy.Field()
    ref = scrapy.Field()
    url = scrapy.Field()
    email = scrapy.Field()
