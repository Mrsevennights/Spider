# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .items import QdBookListItem

class QdspiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_uri=crawler.settings.get("MONGO_URI")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, QdBookListItem):
            self._process_bookList_item(item)
        else:
            self._process_bookDetail_item(item)

        return item

    def _process_bookList_item(self, item):
        self.db.book.insert(dict(item))

    def _process_bookDetail_item(self, item):
        self.db.bookDetail.insert(dict(item))
