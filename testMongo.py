# encoding: utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('10.0.0.168', 27017)
db = client['physics']
res = db.collection_names()
print res