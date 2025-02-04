from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()

LLM_MODEL = os.getenv('LLM_MODEL')
LLM_TEMPERATURE = int(os.getenv('LLM_TEMPERATURE'))

def get_llm():
    llm = ChatOllama(
        model = LLM_MODEL,
        temperature= LLM_TEMPERATURE
    )
    
    return llm  