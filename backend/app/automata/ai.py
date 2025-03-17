from langchain_community.document_loaders import PyPDFLoader
from uuid import uuid4
from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from ..config import *
from .template import templates

embeddings = OllamaEmbeddings(model=LLM_MODEL)

def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,  
        chunk_overlap=20,  
        add_start_index=True,   
    )
        
    return text_splitter

def get_vectore_store(collection_name='default-collection'):
    vector_store = PGVector(
        connection=CONNECTION_STRING,
        collection_name=collection_name,
        embeddings=embeddings,
        use_jsonb=True
    )

    return vector_store

def save_document(document, collection_name):
    if collection_name is not None:   
        vector_store = get_vectore_store(collection_name=str(document.user_id))
        
        doc_pages = doc_load(document=document)
        
        doc_pages = add_metadata(doc_pages=doc_pages, document=document)
        
        store_docs(vector_store=vector_store, docs=doc_pages)
        
def split_docs(documents):
    text_splitter = get_text_splitter()
    return text_splitter.split_documents(documents) 

def add_metadata(doc_pages, document):
    for doc_p in doc_pages:
        doc_p.metadata['user_id'] = document.user_id
        doc_p.metadata['document_id'] = document.id
        
    return doc_pages

def store_docs(vector_store, docs):
    uuids = [str(uuid4()) for x in docs]
    vector_store.add_documents(documents=docs, ids=uuids)
    
def retrieve_by_metadata(vector_store, md_filter):
    retrieved_docs = vector_store.similarity_search(filter=md_filter)
    return retrieved_docs

def retrieve(vector_store, question, db_filter):
    retrieved_docs = vector_store.similarity_search(question, k=3, filter=db_filter)
    return retrieved_docs 

def doc_load(document):
    doc_path = f"{DOCS_ROOT}/{document.hashname}.pdf" 
    loader = PyPDFLoader(doc_path)
    pages = []
    
    for page in loader.lazy_load():
        pages.append(page)
            
    return pages 

@tool
def retrieve_document_context(user_id: int, question: str) -> str:
    """Returns the context for a question by looking at the documents stored in the database relative to the user id

    Args:
        user_id (int): the user ID.
        question (str): Base question to search the context for.
    """
    
    vector_store = get_vectore_store(str(user_id))
    query_result, scores = zip(*vector_store.similarity_search_with_score(query="Emanuele Muzio", k=3, filter={"user_id" : 3}))
    
    context = "\n\n".join(doc.page_content for (doc, score) in zip(query_result, scores) if score > .5)
    
    return context

tools = [retrieve_document_context]

def create_chat_model():
    chat_model = init_chat_model(LLM_MODEL, model_provider=MODEL_PROVIDER)
    
    return chat_model.bind_tools(tools) 

def create_agent():
    agent = create_react_agent(create_chat_model(), tools)
    
    return agent

def metadata_to_context(metadata:dict) -> str:
    return " ".join([f"{x} : {y}" for (x, y) in metadata.items()])
    
def invoke(question : str, metadata : dict):
    
    context = metadata_to_context(metadata=metadata)
    agent = create_agent()
    prompt = ChatPromptTemplate.from_template(template=templates[LLM_TEMPLATE]).invoke({
        "question" : question,
        "language" : LANGUAGE,
        "context" : context
    })
     
    result = agent.invoke(prompt) 
    
    return result["messages"][-1].content  

#TODO: Aggiungere memoria