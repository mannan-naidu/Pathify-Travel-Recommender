# backend/app/__init__.py
from flask import Flask
from pymongo import MongoClient
from celery import Celery
from .config import Config
from flask_cors import CORS  # <-- ADD THIS MISSING IMPORT

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client[Config.MONGO_DB_NAME]

# Initialize Celery with lowercase config names
celery = Celery(__name__,
                broker=Config.broker_url,
                backend=Config.result_backend)

# Explicitly tell Celery where to find tasks
celery.conf.imports = ("app.tasks",)

def create_app():
    app = Flask(__name__)
    CORS(app) # This line will now work

    # Update Flask config from our Config object
    app.config.from_object(Config)
    
    # Update Celery config from Flask's config
    celery.conf.update(app.config)

    from . import routes
    app.register_blueprint(routes.main)

    return app