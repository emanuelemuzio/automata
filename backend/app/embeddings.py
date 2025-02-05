from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

LLM_MODEL = os.getenv('LLM_MODEL')

def get_embeddings():
    embeddings = OllamaEmbeddings(model=LLM_MODEL)
    
    return embeddings