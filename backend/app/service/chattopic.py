from ..service.auth import *
from ..service.documents import *
from ..model.ChatTopic import ChatTopic
from ..model.Chat import Chat

def create_chat_topic(topic_name : str, user_id : int, session):
    
    topic_count = session.exec(
        select(ChatTopic)
        .where(ChatTopic.user_id == user_id)
    ).all()
    
    if len(topic_count) >= 10: 
        raise HTTPException(status_code=400, detail="Limite massimo di 10 chat raggiunto.")

    topic = ChatTopic(name=topic_name, user_id=user_id)
    
    session.add(topic)
    session.commit()
    session.refresh(topic)
    
    return topic
    
def get_user_topics(user_id : int, session):
    
    topics = session.exec(
        select(ChatTopic)
        .where(ChatTopic.user_id == user_id)
        .order_by(ChatTopic.created_at.asc())
    ).all()
    
    return topics

def get_topic(topic_id : int, session):
    topic = session.exec(
        select(ChatTopic)
        .where(ChatTopic.id == topic_id)
    ).one_or_none()
    
    return topic

def update_chat_topic(new_name : str, topic_id : int, user_id : int, session):
    topic = session.exec(
        select(ChatTopic)
        .where(ChatTopic.id == topic_id)
        .where(ChatTopic.user_id == user_id)
    ).one_or_none()
    
    topic.name = new_name
    
    session.add(topic)
    session.commit()
    session.refresh(topic)
    
def delete_topic(topic_id : int, user_id : int, session):
    topic = session.exec(
        select(ChatTopic)
        .where(ChatTopic.id == topic_id)
        .where(ChatTopic.user_id == user_id)
    ).one_or_none()
    
    chat_topic_history = session.exec(
        select(Chat)
        .where(Chat.topic_id == topic_id)
    ).all()
    
    for chat in chat_topic_history:
        session.delete(chat)
    
    session.delete(topic)
    session.commit()