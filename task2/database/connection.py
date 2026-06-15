from pymongo import MongoClient

from config.settings import (
    MONGO_URI,
    MONGO_DB_NAME
)

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]