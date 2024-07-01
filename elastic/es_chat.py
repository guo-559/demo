from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import gradio as gr
from langchain.schema import AIMessage, HumanMessage
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings
import os

from pathlib import Path

load_dotenv(dotenv_path='./elastic.env')

# TODO: refactor nicely. For now, this rag chatbot is self-contained

username = os.getenv('ELASTIC_USERNAME')
password = os.getenv('ELASTIC_PASSWORD')
elastic_url = os.getenv('ELASTIC_URL')
elastic_index = os.getenv('ES_INDEX')


llm = ChatNVIDIA(model="meta/llama3-8b-instruct", 
                 streaming=True
)

# TODO: use a free embedding model
vector_store = ElasticsearchStore(elastic_index, 
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"), 
    es_url=elastic_url, es_user=username, es_password=password)

# TODO: do you need system prompt?
def predict(message, history):
    history_langchain_format = []

    try:
        for human, ai in history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
        

        # TODO: adds retrieved data here. This is very crude, needs to be improved
        # need chunking and stuff. look into Langchain's LCEL etc.
        # TODO: modify the number of documents returned
        docs = vector_store.as_retriever().invoke(message)
        retrieved_data = ""
        for doc in docs:
            retrieved_data += doc.page_content

        print('RETRIEVED', retrieved_data)

        history_langchain_format.append(HumanMessage(content=retrieved_data + message))

        partial_msg = ""
        for chunk in llm.stream(history_langchain_format):
            partial_msg += chunk.content
            yield partial_msg
    except:
        # TODO: This is to reset the history when we exceed the context window
        # Is there a more graceful way to handle this? 
        print('dumping history...')
        history = []
        history_langchain_format = []


# Adds uploaded files to the vector database
def upload_and_vectorize(files):
    file_paths = [file.name for file in files]
    documents = []

    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')

            """
            TODO: add the metadata later
            documents.append({
                "file_name": file_path,
                "content": content
            })

            """
            documents.append(content)
    
    # TODO: what's the difference?
    # vector_store.add_documents(documents)
    vector_store.add_texts(documents)
    return file_paths

with gr.Blocks(fill_height=True) as demo:
    gr.Markdown(
        """
        # Example RAG
        Start talking to the chatbot below.
        """
    )
    gr.ChatInterface(predict)

    # TODO: Make this shit look less ugly
    file_output = gr.File()
    ub = gr.UploadButton("Upload a file", file_count="multiple")
    ub.upload(upload_and_vectorize, ub, file_output)

demo.launch()
