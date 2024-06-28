import uuid
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv(dotenv_path='./elastic.env')
username = os.getenv('ELASTIC_USERNAME')
password = os.getenv('ELASTIC_PASSWORD')
elastic_url = os.getenv('ELASTIC_URL')

client = Elasticsearch(
    elastic_url,
    basic_auth=(username, password)
)

print(client.info())

document_id = str(uuid.uuid4())

# Define the document to be indexed
document = {
    'name': 'Snow Crash',
    'author': 'Neal Stephenson',
    'release_date': '1992-06-01',
    'page_count': 470,
}

# Define the index name
index_name = 'books'

# Delete the index
if client.indices.exists(index=index_name):
    client.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted.")

# Recreate the index (optional)
client.indices.create(index=index_name)
print(f"Index '{index_name}' created.")

# Index the document
response = client.index(index=index_name, document=document)

# Print the response
print(response)

# Define the search query
search_query = {
    "query": {
        "match": {
            "author": "Neal Stephenson"
        }
    }
}

# Perform the search
response = client.search(index="books", body=search_query)


print("\n Getting response \n")
# Print the response
print(response)