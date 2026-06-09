# backend/app/__init__.py
from flask import Flask
from pymongo import MongoClient
from celery import Celery
from .config import Config
from flask_cors import CORS  # <-- ADD THIS MISSING IMPORT

import ssl

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client[Config.MONGO_DB_NAME]

# Initialize Celery with lowercase config names
celery = Celery(__name__,
                broker=Config.broker_url,
                backend=Config.result_backend)

# Explicitly tell Celery where to find tasks
celery.conf.imports = ("app.tasks",)

# Programmatically configure SSL cert requirements for secure Redis connections
if Config.broker_url and Config.broker_url.startswith("rediss://"):
    celery.conf.broker_use_ssl = {'ssl_cert_reqs': ssl.CERT_NONE}
if Config.result_backend and Config.result_backend.startswith("rediss://"):
    celery.conf.redis_backend_use_ssl = {'ssl_cert_reqs': ssl.CERT_NONE}


def create_app():
    app = Flask(__name__)
    CORS(app) # This line will now work

    # Update Flask config from our Config object
    app.config.from_object(Config)
    
    # Update Celery config from Flask's config
    celery.conf.update(app.config)

    # Test MongoDB connection on startup
    try:
        mongo_client.admin.command('ping')
        print(f" * Successfully connected to MongoDB database: '{Config.MONGO_DB_NAME}'")
    except Exception as e:
        print(f" * ERROR: Failed to connect to MongoDB: {e}")

    from . import routes
    app.register_blueprint(routes.main)

    return app