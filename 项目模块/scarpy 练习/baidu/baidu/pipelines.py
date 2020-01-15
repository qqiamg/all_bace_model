# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 用于数据处理（存储数据等）

class BaiduPipeline(object):
    def process_item(self, item, spider):
        return item
