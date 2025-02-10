from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from uuid import uuid4
from .template import templates
from .state import State

class Automata:

    embeddings = None 
    prompt = None
    text_splitter = None
    vector_store = None
    llm = None
    docs_root = None
    template = None
    valid_content_types= None
    config = {}
    
    def __init__(self, config, allowed_content_types):
        

        self.config = config

        if config['LLM_TEMPLATE'] is None:
            self.prompt = self.hub_pull()
        else:
            self.prompt = self.get_wrapper(config['LLM_TEMPLATE'])
            
        self.text_splitter = self.get_text_splitter()
        self.llm = self.get_llm()
        self.wrapper = self.get_wrapper()
        self.docs_root = config['DOCS_ROOT']
        self.allowed_content_types = allowed_content_types
        self.embeddings = self.get_embeddings()
        
    def add_metadata(self, doc_pages, document):
        
        for doc_p in doc_pages:
            doc_p.metadata['user_id'] = document.user_id
            doc_p.metadata['document_id'] = document.id
        
        return doc_pages
        
    def save_document(self, document, collection_name):
        
        if collection_name is not None:   
            self.vector_store = self.get_vectore_store(collection_name=str(document.user_id))
        else:
            self.vector_store = self.get_vectore_store()
        
        doc_pages = self.doc_load(document)
        
        doc_pages = self.add_metadata(doc_pages, document)
        
        self.store_docs(doc_pages)
        
    def split_docs(self, documents):
        
        return self.text_splitter.split_documents(documents) 
            
    def doc_load(self, document):
        
        doc_path = f"{self.docs_root}/{document.hashname}.pdf" 
        
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
        
    def retrieve(self, state : State):
        
        self.vector_store = self.get_vectore_store(collection_name=state['collection'])
        
        retrieved_docs = self.vector_store.similarity_search(state['question'], k=3, filter=state['db_filter'])
        
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
    
    def get_vectore_store(self, collection_name='default-collection'):

        vector_store = PGVector(
            connection=self.config['CONNECTION_STRING'],
            collection_name=collection_name,
            embeddings=self.embeddings,
            use_jsonb=True
        )
    
        return vector_store 

    def get_embeddings(self):
        
        embeddings = OllamaEmbeddings(model=self.config['LLM_MODEL'])
        
        return embeddings 

    def get_llm(self):
        
        llm = ChatOllama(
            model = self.config['LLM_MODEL'],
            temperature= int(self.config['LLM_TEMPERATURE'])
        )
        
        return llm  

    def hub_pull(self):
        
        prompt = hub.pull(self.config['RAG_PROMPT'])
        return prompt
            
    def get_wrapper(self, template_name="template-1"):
        
        template = templates[template_name]
        
        return PromptTemplate.from_template(template)

    def get_text_splitter(self):
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  
            chunk_overlap=150,  
            add_start_index=True,   
        )
        
        return text_splitter