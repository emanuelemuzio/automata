from langchain_community.document_loaders import PyPDFLoader
from embeddings import get_embeddings
from rag import hub_pull, get_wrapper
from text_splitter import get_text_splitter
from vector_store import get_vectore_store
from uuid import uuid4
from llm import get_llm
from state import State
from doc_loader import DOCS_ROOT

class Automata:

    embeddings = None 
    prompt = None
    text_splitter = None
    vector_store = None
    llm = None
    docs_root = None
    template = None
    
    def __init__(self, template=None):
        self.embeddings = get_embeddings()
        
        if template is None:
            self.prompt = hub_pull()
        else:
            self.prompt = get_wrapper(template)
            
        self.text_splitter = get_text_splitter()
        self.vector_store = get_vectore_store()
        self.llm = get_llm()
        self.wrapper = get_wrapper()
        self.docs_root = DOCS_ROOT 
        
    def save_document(self, document_name):
        doc_pages = self.doc_load(document_name)
        doc_stored = self.store_docs(doc_pages)
        
        return True
        
    def split_docs(self, documents):
        return self.text_splitter.split_documents(documents)
            
    def doc_load(self, doc_name):
        
        doc_path = f"{self.docs_root}/{doc_name}"
        
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
        uuids = [str(uuid4()) for _ in range(len(docs))]
    
        vector_store = get_vectore_store()
        vector_store.add_documents(documents=docs, ids=uuids)
        
        return True
    
    def retrieve(self, state : State):
        retrieved_docs = self.vector_store.similarity_search(state['question'], k=2)
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
        
automata = Automata(template='template-1')
test_state = State({"question" : "Cosa sono le compresse?"})
response = automata.invoke(test_state)
print(response['answer'])