from pymongo import MongoClient
from django.conf import settings

db = settings.DATABASES['mongo'].get("NAME")
mongo_database = {
    "host": settings.DATABASES['mongo'].get("CLIENT", {}).get("host"),
    "port": settings.DATABASES['mongo'].get("CLIENT", {}).get("port"),
    "username": settings.DATABASES['mongo'].get("CLIENT", {}).get("username"),
    "password": settings.DATABASES['mongo'].get("CLIENT", {}).get("password"),
}
mongo_client = MongoClient(**mongo_database)
mongo_default_db = mongo_client[db]