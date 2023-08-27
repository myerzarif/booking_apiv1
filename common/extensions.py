from pymongo import MongoClient
from django.conf import settings

db = settings.MONGO_DB_SETTING.get("NAME")
mongo_database = {
    "host": settings.MONGO_DB_SETTING.get("CLIENT", {}).get("host"),
    "port": settings.MONGO_DB_SETTING.get("CLIENT", {}).get("port"),
    "username": settings.MONGO_DB_SETTING.get("CLIENT", {}).get("username"),
    "password": settings.MONGO_DB_SETTING.get("CLIENT", {}).get("password"),
}
mongo_client = MongoClient(**mongo_database)
mongo_default_db = mongo_client[db]
