# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    broker_url = os.getenv("broker_url")
    result_backend = os.getenv("result_backend")