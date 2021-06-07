import pymongo, os
from dotenv import load_dotenv


load_dotenv()

class Database:
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
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
