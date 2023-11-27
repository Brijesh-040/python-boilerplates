from pymongo import MongoClient
from pymongo.collation import Collation, CollationStrength

client = MongoClient("mongodb://localhost:27017/demo_python")
db = client.get_database()