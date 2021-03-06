# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .db.database import Database
import os


class HrPipeline(object):
    def __init__(self):
        self._db = Database(os.environ['DATABASE_URL'])

    def process_item(self, item, _spider):
        item.setdefault('email', None)
        item.setdefault('ref', None)

        if item.get('date'):
            self._db.find_or_create(item)
        return item
