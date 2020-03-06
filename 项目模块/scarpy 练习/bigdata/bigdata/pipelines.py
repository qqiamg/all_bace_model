# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.conf import settings #老版写法
from scrapy.utils.project import get_project_settings #新版写法
import logging
# from bigdata import settings

class BigdataPipeline(object):
    def process_item(self, item, spider):
        return item

class PipelineMongodb(object):
    def open_spider(self,spider):
        try:
            settings = get_project_settings()
            host = settings['MONGODB_HOST']
            port = settings['MONGODB_PORT']
            self.client = pymongo.MongoClient(host=host, port=port)
            self.collection = self.client[settings['MONGODB_DB']]
        except Exception as e:
            logging.log(logging.ERROR,'PipelineMongodb open_spider: ' + str(e))

    def process_item(self, item, spider):
        try:
            table_name = '测试'
            collection = self.collection[table_name]
            collection.insert_one(dict(item))
        except Exception as e:
            logging.log(logging.ERROR, 'PipelineMongodb process_item: ' + str(e))
        return item

    def close_spider(self, spider):
        try:
            self.client.close()
        except Exception as e:
            logging.log(logging.ERROR, 'PipelineMongodb close_spider: ' + str(e))
