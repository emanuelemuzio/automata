from ..model.User import User
from ..service.auth import *
from ..service.documents import *
from sqlalchemy import cast, Integer 
from ..common import AutomataState
from ..model.Chat import Chat
from ..response import ChatResponse

def invoke_automata(question : str, topic_id : int, user : User, session) -> ChatResponse:
    
    db_filter = {
        "user_id" : user.id
    }
    
    state = AutomataState({
        "question" : question, 
        "db_filter" : db_filter, 
        "collection" : str(user.id)
    })
    
    # response = automata.invoke(state)
    response = {
        'answer' : 'test'
    }
        
    chat_message = Chat(question=question, answer=response['answer'], user_id=user.id, topic_id=topic_id)
    
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    
    chat_response = ChatResponse(answer=response['answer'])
    
    return chat_response