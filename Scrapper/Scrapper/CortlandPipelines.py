import pymongo
import sys


class ScrapperPipeline:

    def __init__(self):
        self.collection = "cortland_products"
        self.mongodb_uri = "mongodb+srv://admin:admin1@atlascluster.5r0ou.mongodb.net/?retryWrites=true&w=majority"
        self.mongodb_db = "apple_products"
        if not self.mongodb_uri:
            sys.exit("No conn string set")

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        self.db[self.collection].insert_one(data)
        return item
