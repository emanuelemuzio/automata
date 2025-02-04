from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os

load_dotenv()

DOCS_ROOT = f"{os.getcwd()}\\{os.getenv('DOCS_ROOT')}" 

def doc_load(file_path : str):
    
    loader = PyPDFLoader(file_path)
    pages = []
    for page in loader.lazy_load():
        pages.append(page)
        
    return pages