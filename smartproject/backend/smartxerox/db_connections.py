import pymongo 
from pymongo import MongoClient

url='mongodb://localhost:27017'

client= pymongo.MongoClient(url)
database = client["smart_xerox_db"]

import mongoengine
mongoengine.connect(
    db='smart_xerox_db',
    host='mongodb://localhost:27017',
    username='<admin>',
    password='<admin>'
)