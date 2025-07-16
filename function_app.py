import azure.functions as func
from pymongo import MongoClient
import os
import logging
import json

app = func.FunctionApp()

# MongoDB URI from Cosmos (replace <password> securely)
MONGO_URI = os.environ["MONGO_URI"]  # use local.settings.json or env var

client = MongoClient(MONGO_URI)
db = client["LibraryDB"]  # Replace with your DB name
collection = db["Books"]  # Replace with your collection name

# Function to return all books sorted by dateAdded descending


@app.route(route="add_book", auth_level=func.AuthLevel.ANONYMOUS)
def add_book(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        book = {
            'id': req_body.get('id'),
            'title': req_body.get('title'),
            'author': req_body.get('author'),
            'genre': req_body.get('genre'),
            'format': req_body.get('format'),
            'location': req_body.get('location'),
            'readStatus': req_body.get('readStatus', 'Unread'),
            'dateAdded': req_body.get('dateAdded'),
            'lastUsed': req_body.get('lastUsed'),
            'rating': req_body.get('rating'),
            'notes': req_body.get('notes')
        }

        collection.insert_one(book)

        return func.HttpResponse(f"Book added: {book['title']}", status_code=201)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
