from ..model.LangChainEmbedding import LangChainEmbedding
from ..service.auth import *
from ..service.documents import *
from ..config import *
from ..model.Document import Document
from ..automata.ai import *
from sqlalchemy import cast, Integer
from uuid import uuid4
from typing import Sequence
from pathlib import Path
from sqlalchemy.exc import InternalError
from fastapi.responses import FileResponse

def is_valid_content_type(content_type, allowed_content_types):
    return content_type in allowed_content_types

def cascade_document(document, vector_session):
    
    statement = select(LangChainEmbedding).where(
        cast(LangChainEmbedding.cmetadata["document_id"].astext, Integer) == document.id
    )
    
    embeddings = vector_session.exec(statement).all()
    
    for e in embeddings:
        vector_session.delete(e)  
        
def document_upload(file, user_id, username, session): 
    try:
        if is_valid_content_type(file.content_type, allowed_content_types):
            
            document = Document(
                filename=file.filename,
                extension=file.content_type,
                visible=True,
                user_id=user_id
            )
            
            results = session.exec(
                select(Document)
                .where(Document.filename == file.filename) 
                .where(Document.user_id == user_id) 
                ).all()
            
            if len(results) > 0:
                raise HTTPException(
                    status_code=status.HTTP_208_ALREADY_REPORTED, 
                    detail="A file with that name is already present"
                )
            
            hashed_name = f"{str(uuid4())}"
            collection_name = username
            
            document.hashname = hashed_name
            
            file_location = f'{DOCS_ROOT}/{hashed_name}.pdf'
            
            Path(DOCS_ROOT).mkdir(parents=True, exist_ok=True)
            
            with open(file_location, 'wb+') as file_object:
                file_object.write(file.file.read())
                                             
            session.add(document)
            session.commit()
            session.refresh(document)
            
            save_document(document, collection_name)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )
    except InternalError: 
        
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown error"
            )
        
def get_user_documents(user_id: int, session) -> Sequence[Document]:
    
    document_list = session.exec(
        select(Document)
        .where(Document.user_id == user_id)
        .order_by(Document.created_at.asc())
    ).all()
    
    return document_list

def download(document_id : int, user_id : int, session) -> FileResponse:
    
    document = session.exec(
        select(Document)
        .where(Document.id == document_id)
        .where(Document.user_id == user_id)
        ).one_or_none()
    
    if document is None:
        raise HTTPException(status_code=404, detail="Documento non trovato, record non presente")
    
    document_path = f"{DOCS_ROOT}/{document.hashname}.pdf"
    
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Documento non trovato, file non presente")

    return FileResponse(document_path, filename=os.path.basename(document_path), media_type="application/pdf")

def delete(document_id : int, user_id : int, session, vector_session):
    
    try:
        document = session.exec(
            select(Document)
            .where(Document.id == document_id) 
            .where(Document.user_id == user_id)
        ).one()
         
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    cascade_document(document, vector_session)
        
    session.delete(document)
    vector_session.commit()
    session.commit()
    
    os.remove(f"{DOCS_ROOT}/{document.hashname}.pdf") 