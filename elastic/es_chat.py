from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import gradio as gr
from langchain.schema import AIMessage, HumanMessage


load_dotenv(dotenv_path='./elastic.env')

llm = ChatNVIDIA(model="meta/llama3-8b-instruct", 
                 streaming=True
)

def predict(message, history):

    print('predicting...')

    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))

    partial_msg = ""
    for chunk in llm.stream(history_langchain_format):
        partial_msg += chunk.content
        yield partial_msg

gr.ChatInterface(predict).launch()