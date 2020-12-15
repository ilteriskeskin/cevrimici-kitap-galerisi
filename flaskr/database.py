import pymongo
import os


class db(object):
    user = 'kitapci'
    name = 'kitapci'
    pw = 'MemurBeySelcuk'
    URI = "mongodb://kitapci:MemurBeySelcuk@kitapci-shard-00-00.xnez1.mongodb.net:27017,kitapci-shard-00-01.xnez1.mongodb.net:27017,kitapci-shard-00-02.xnez1.mongodb.net:27017/kitapci?ssl=true&replicaSet=atlas-xpk9te-shard-0&authSource=admin&retryWrites=true&w=majority"

    @staticmethod
    def init():
        client = pymongo.MongoClient(db.URI)
        db.DATABASE = client[db.name]

    @staticmethod
    def insert(collection, data):
        db.DATABASE[collection].insert(data)

    def insert_one(collection, data):
        return db.DATABASE[collection].insert_one(data)

    @staticmethod
    def find_one(collection, query):
        return db.DATABASE[collection].find_one(query)

    def find(collection, query):
        return db.DATABASE[collection].find(query)

    def find_and_modify(collection, query, **kwargs):
        print(kwargs)
        db.DATABASE[collection].find_and_modify(query=query,
                                                update={"$set": kwargs}, upsert=False,
                                                full_response=True)