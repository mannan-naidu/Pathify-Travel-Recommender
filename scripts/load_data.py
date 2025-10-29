# (scripts)/load_data.py
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../backend/.env') # Path to the .env file

print(f"DEBUG: MONGO_URI = {os.getenv('MONGO_URI')}")

def load_data_to_mongo():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB_NAME")]
    collection = db['pois']

    # Clear existing data
    collection.delete_many({})

    # Load from JSON file
    with open('mumbai_pois.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert into MongoDB
    collection.insert_many(data)
    print(f"Successfully loaded {len(data)} documents into the 'pois' collection.")

if __name__ == "__main__":
    load_data_to_mongo()