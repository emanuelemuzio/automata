from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  
        chunk_overlap=150,  
        add_start_index=True,   
    )
    return text_splitter

def split_document(doc):
    text_splitter = get_text_splitter()
    return text_splitter.split_documents(doc)