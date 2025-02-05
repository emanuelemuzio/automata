from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from uuid import uuid4

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str 
    collection_name: str