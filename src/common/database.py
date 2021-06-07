import pymongo


class Database:
    URI="mongodb+srv://zhaoyufrank8825:yingying8825@cluster0.x1tdu.mongodb.net/test"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["myblog"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
    
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
