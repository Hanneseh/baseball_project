from pymongo import MongoClient

def getDB():
    client = MongoClient('mymongo', 27017)
    return client