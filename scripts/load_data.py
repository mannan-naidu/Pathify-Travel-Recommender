# (scripts)/load_data.py
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env file relative to the script location
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(basedir, '../backend/.env'))


print(f"DEBUG: MONGO_URI = {os.getenv('MONGO_URI')}")

def load_data_to_mongo():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB_NAME")]
    collection = db['pois']

    # Clear existing data
    collection.delete_many({})

    # Load from JSON file
    json_path = os.path.join(basedir, 'mumbai_pois.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert into MongoDB
    collection.insert_many(data)
    print(f"Successfully loaded {len(data)} documents into the 'pois' collection.")

if __name__ == "__main__":
    load_data_to_mongo()