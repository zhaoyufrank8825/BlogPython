import pymongo

uri = "mongodb://127.0.0.1:27017"
client = pymongo.MongoClient(uri)
print("connect to database successfully.")
database = client['zhaoyu']
collection = database['books']

books = collection.find({})
print("It is here.")

for book in books:
    print(book)
