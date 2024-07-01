import uuid
import os
from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv(dotenv_path='./elastic.env')
username = os.getenv('ELASTIC_USERNAME')
password = os.getenv('ELASTIC_PASSWORD')
elastic_url = os.getenv('ELASTIC_URL')
elastic_index = os.getenv('ES_INDEX')


# This file just gives examples of how to interact with the elasticsearch
# database. The actual chat application is in another file.

client = Elasticsearch(
    elastic_url,
    basic_auth=(username, password)
)

print(client.info())
# print(client.cluster.health())
# print(client.cluster.stats())
# print(client.nodes.stats())

index_name = elastic_index

# For deleting the index if u want to restart
#if client.indices.exists(index=index_name):
#    client.indices.delete(index=index_name)
#    print(f"Index '{index_name}' deleted.")


"""

# Recreate the index (optional)
client.indices.create(index=index_name)
print(f"Index '{index_name}' created.")

# Index the document
response = client.index(index=index_name, document=document)

# Print the response
print(response)

"""

# Define the search query
# TODO: fuzzy search?
search_query = {
    "_source": {
        "excludes": ["vector"]
    },
    "query": {
        "match": {'text': "pig"}
    },
    "size": 5
}

# Perform the search
response = client.search(index=index_name, body=search_query)


print("\n Getting response \n")
# Print the response
print(response)

vector_store = ElasticsearchStore(elastic_index, 
                                      embedding=OpenAIEmbeddings(model="text-embedding-3-large"), 
                                      es_url=elastic_url, es_user=username, 
                                      es_password=password, 
                                      )





question = "what wall street news is there?"

print('\n Now testing retrieval for Question: ', question, ' \n')

docs = vector_store.as_retriever().invoke(question)
for doc in docs:
    print(doc.page_content, '\n')
