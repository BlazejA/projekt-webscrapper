# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

# class ScrapperPipeline:
#
#     def __init__(self):
#         # self.conn = pymongo.MongoClient()
#         # db = self.conn['data']
#         # self.collection = db['price']
#         return
#
#     def process_item(self, item, spider):
#         return item
