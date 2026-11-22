
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI no está configurada")

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

database = client["reservaflow"]

def test_connection():
    client.admin.command("ping")
    return True
