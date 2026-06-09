# backend/app/config.py
import os
from dotenv import load_dotenv

# Load the .env file from the backend root directory regardless of where Python is executed
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    broker_url = os.getenv("broker_url")
    result_backend = os.getenv("result_backend")