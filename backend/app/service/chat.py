from ..model.User import User
from ..service.auth import *
from ..service.documents import *
from ..automata.state import State
from ..model.Chat import Chat
from ..response import ChatResponse

def invoke_automata(question : str, topic_id : int, user : User, session) -> ChatResponse:
    
    db_filter = {
        "user_id" : user.id
    }
    
    state = State({
        "question" : question, 
        "db_filter" : db_filter, 
        "collection" : str(user.id)
    })
    
    response = automata.invoke(state)
    
    chat = Chat(question=question, answer=response["answer"], user_id=user.id, topic_id=topic_id)
    
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