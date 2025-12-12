from pymongo import MongoClient, IndexModel, ASCENDING
import os
from dotenv import load_dotenv
import certifi
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

def create_indexes():
    """
    Ensure indexes (run at startup).
    """
    users = db.get_collection("users")
    index = IndexModel([("email", ASCENDING)], unique=True)
    users.create_indexes([index])

def ping_db():
    """
    Simple check to ensure DB is reachable.
    """
    try:
        client.admin.command("ping")
        return True
    except ServerSelectionTimeoutError:
        return False


