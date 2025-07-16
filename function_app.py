import azure.functions as func
from azure.cosmos import CosmosClient
import os
import logging
import json

app = func.FunctionApp()

# Read Cosmos DB settings from environment
COSMOS_ENDPOINT = os.environ['COSMOS_ENDPOINT']
COSMOS_KEY = os.environ['COSMOS_KEY']
DATABASE_NAME = 'LibraryDB'
CONTAINER_NAME = 'Books'

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

@app.route(route="add_book", auth_level=func.AuthLevel.ANONYMOUS)
def add_book(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing add_book request.")

    try:
        req_body = req.get_json()

        book = {
            'id': req_body.get('id'),  # Make sure this is unique
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

        container.create_item(book)

        return func.HttpResponse(
            f"Book added: {book['title']}",
            status_code=201
        )

    except Exception as e:
        logging.error(f"Error in add_book: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
