# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst

DATE_FORMAT = "%Y/%m/%d"


def date_processor(self, values):
    for v in values:
        yield datetime.strptime(v, "%d/%m/%Y").strftime(DATE_FORMAT)


class JobItemLoader(ItemLoader):
    date_in = date_processor

    date_out = TakeFirst()
    text_out = Join()
    ref_out = TakeFirst()
    url_out = TakeFirst()
    email_out = TakeFirst()


class JobItem(scrapy.Item):
    date = scrapy.Field()
    text = scrapy.Field()
    ref = scrapy.Field()
    url = scrapy.Field()
    email = scrapy.Field()
