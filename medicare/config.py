from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "")
    DB_NAME = ""
    GEMINI_API_KEY=""
    @staticmethod
    def get_db():
        client = MongoClient(Config.MONGO_URI)
        return client[Config.DB_NAME]