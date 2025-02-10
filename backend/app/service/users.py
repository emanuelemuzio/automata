from ..config import *
from ..model.User import User
from ..model.Document import Document
from ..model.LangChainCollection import LangChainCollection
from ..model.LangChainEmbedding import LangChainEmbedding
from ..service import auth as auth_service
from ..service.documents import *
from sqlalchemy.exc import ProgrammingError

def cascade_user(user, session, vector_session):
    document_list = session.exec(select(Document).where(Document.user_id == user.id)).all()
    
    for document in document_list:
        cascade_document(document, vector_session)
        session.delete(document)
        
    try:    
        collection = vector_session.exec(select(LangChainCollection).where(LangChainCollection.name == str(user.id))). one_or_none()
        
        if collection is not None:
        
            embeddings = vector_session.exec(select(LangChainEmbedding).filter(LangChainEmbedding.collection_id == collection.uuid)).all()
            
            for e in embeddings:
                vector_session.delete(e)
                
            vector_session.delete(collection)

    except ProgrammingError:
        print("Langchain Vector Tables have not been created yet")
        
def create_new_user(
    username,
    full_name,
    password, 
    role,
    session
):
    user = User(
        username=username,
        full_name=full_name,
        pwd=password,
        role=role
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user
    
def update_user(user_id, username, full_name, role, session):
    user_entity = session.exec(
        select(User)
        .where(User.id == user_id)
    ).one()
        
    user_entity.username = username
    user_entity.full_name = full_name
    user_entity.role = role
         
    session.add(user_entity)
    session.commit()
    
def get_all_users(session):
    users_list = session.exec(
        select(User)
        .order_by(User.created_at.asc())
    ).all()
    
    return users_list

def delete_user(user_id : int, session, vector_session):
    user = session.exec(select(User).where(User.id == user_id)).one()
            
    cascade_user(user, session, vector_session)
            
    session.delete(user)
    session.commit()
    
def toggle_user(user_id : int, session):
    user = session.exec(select(User).where(User.id == user_id)).one()
            
    user.disabled = not user.disabled
            
    session.add(user)
    session.commit()
    
def update_password(user_id, new_password, session):
    user = session.exec(select(User).where(User.id == user_id)).one()
            
    user.pwd = auth_service.get_password_hash(new_password)
            
    session.add(user)
    session.commit()
    session.refresh(user)