"""
db.py
MongoDB connection and data access for the Radiology Annotation Tool.

Stores every annotation as a document in the `annotations` collection,
replacing the previous CSV-based storage with a real database backend.
"""

import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file (not committed to git)

# Connection string is read from the .env file — never hardcode credentials here
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "radiology_annotations"
COLLECTION_NAME = "annotations"

_client = None


def get_collection():
    """Return the MongoDB collection, creating the connection once and reusing it."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client[DB_NAME][COLLECTION_NAME]


def insert_annotation(annotation: dict):
    """Insert one annotation document into MongoDB."""
    collection = get_collection()
    collection.insert_one(annotation)


def fetch_annotations_df(scan_type: str = None) -> pd.DataFrame:
    """
    Fetch annotations from MongoDB as a pandas DataFrame,
    so the rest of the app (validation dashboard) can keep using
    the same DataFrame-based logic it already had with CSV.
    """
    collection = get_collection()
    query = {} if not scan_type or scan_type == "All" else {"scan_type": scan_type}
    docs = list(collection.find(query, {"_id": 0}))
    return pd.DataFrame(docs)


def update_annotation_metadata(filename: str, timestamp: str, updates: dict):
    """
    Correct metadata fields (e.g. label, notes, confidence) on an
    existing annotation, identified by filename + timestamp.
    Used by the metadata-correction workflow in the validation dashboard.
    """
    collection = get_collection()
    collection.update_one(
        {"filename": filename, "timestamp": timestamp},
        {"$set": updates}
    )