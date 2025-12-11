from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)

db = client.fastapi_db

try:
    client.admin.command('ping')
    print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)

def get_collection(name: str):
    return db[name]


