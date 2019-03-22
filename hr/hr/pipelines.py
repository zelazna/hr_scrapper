# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .db.database import Database


class HrPipeline(object):
    def __init__(self):
        self._db = Database()

    def process_item(self, item, _spider):
        self._db.save(item)
        return item
