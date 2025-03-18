from ..model.User import User
from ..service.auth import *
from ..service.documents import *
from ..model.Chat import Chat
from ..response import ChatResponse
from ..automata import ai

def invoke(question : str, topic_id : int, user : User, session) -> ChatResponse:
    
    metadata = {
        "user_id" : user.id,
        "topic_id" : topic_id
    }
    
    response = ai.invoke(question=question, metadata=metadata) 
    
    chat = Chat(question=question, answer=response, user_id=user.id, topic_id=topic_id)
    
    session.add(chat)
    session.commit()
    session.refresh(chat)
    
    return chat

def retrieve_chat_history(topic_id : int, user_id : int, session):
    history = session.exec(
        select(Chat)
        .where(Chat.topic_id == topic_id)
        .where(Chat.user_id == user_id)
        .order_by(Chat.created_at.asc())
        ).all()
    
    return history