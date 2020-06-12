import os
from pymongo import MongoClient

def getDB():
    client = MongoClient('localhost', 27017)
    return client