from langchain_community.document_loaders import PyPDFLoader
from embeddings import get_embeddings
from rag import hub_pull, get_wrapper
from text_splitter import get_text_splitter
from vector_store import get_vectore_store
from llm import get_llm
from state import State
from doc_loader import DOCS_ROOT
from uuid import uuid4

class Automata:

    embeddings = None 
    prompt = None
    text_splitter = None
    vector_store = None
    llm = None
    docs_root = None
    template = None
    valid_content_types= None
    
    def __init__(self, template=None):
        self.embeddings = get_embeddings()
        
        if template is None:
            self.prompt = hub_pull()
        else:
            self.prompt = get_wrapper(template)
            
        self.text_splitter = get_text_splitter()
        self.llm = get_llm()
        self.wrapper = get_wrapper()
        self.docs_root = DOCS_ROOT 
        self.allowed_content_types = [ 
            "application/pdf"
        ]
        
    def add_metadata(self, doc_pages, document):
        for doc_p in doc_pages:
            doc_p.metadata['user_id'] = document.user_id
            doc_p.metadata['document_id'] = document.id
        
        return doc_pages
        
    def save_document(self, document, collection_name):
        
        if collection_name is not None:   
            self.vector_store = get_vectore_store(collection_name=str(document.user_id))
        else:
            self.vector_store = get_vectore_store()
        
        doc_pages = self.doc_load(document)
        
        doc_pages = self.add_metadata(doc_pages, document)
        
        doc_stored = self.store_docs(doc_pages)
        
        return doc_pages
        
    def split_docs(self, documents):
        return self.text_splitter.split_documents(documents) 
            
    def doc_load(self, document):
        
        doc_path = f"{DOCS_ROOT}/{document.hashname}.pdf" 
        
        loader = PyPDFLoader(doc_path)
        pages = []
        for page in loader.lazy_load():
            pages.append(page)
            
        return pages
    
    def invoke(self, state : State):
        state['context'] = self.retrieve(state)
        state['answer'] = self.generate(state)
        return state
    
    def store_docs(self, docs):
        uuids = [str(uuid4()) for x in docs]
        
        self.vector_store.add_documents(documents=docs, ids=uuids)
        
        return True
    
    def retrieve(self, state : State):
        
        self.vector_store = get_vectore_store(collection_name=state['collection'])
        
        retrieved_docs = self.vector_store.similarity_search(state['question'], k=3, filter=state['db_filter'])
        
        print(state['db_filter'])
        
        return retrieved_docs
    
    def retrieve_by_metadata(self, md_filter):
        retrieved_docs = self.vector_store.similarity_search(filter=md_filter)
        return retrieved_docs
        
    def generate(self, state : State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        
        messages = self.prompt.invoke(
            { 
                "question": state["question"], 
                "context": docs_content
            }
        )
        
        response = self.llm.invoke(messages)
        return response.content 