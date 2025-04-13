from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://md570:thiwanka%40570MongoDb@cluster0.ys1pg.mongodb.net/url_shortner?retryWrites=true&w=majority&appName=Cluster0")
    DB_NAME = "medicare"
    GEMINI_API_KEY="AIzaSyAvbhHecGbjoM9W58nPHhAk1ZEx-SytwqY"
    @staticmethod
    def get_db():
        client = MongoClient(Config.MONGO_URI)
        return client[Config.DB_NAME]