from fastapi import APIRouter
from typing import Annotated, Sequence
from fastapi import Depends, APIRouter, HTTPException
from ..service.auth import *
from ..service.chat import *
from ..request.ChatRequest import ChatRequest
from ..request.ChatTopicCreate import ChatTopicCreate
from ..response.ChatResponse import ChatResponse
from ..model.ChatTopic import ChatTopic

router = APIRouter()

@router.post("/chat/messages")
async def pose_chat_question(
    session: SessionDep,
    request : ChatRequest,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
) -> ChatResponse:
    response = invoke_automata(request.question, request.topic_id, current_user.id, session) 

    return response
    
@router.post("/chat/topics")
async def create_chat_topic(
    request : ChatTopicCreate, 
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
):
    
    name = request.name

    topic_count = session.exec(
        select(ChatTopic)
        .where(ChatTopic.user_id == current_user.id)
    ).all()
    
    if len(topic_count) >= 10: 
        raise HTTPException(status_code=400, detail="Limite massimo di 10 chat raggiunto.")

    topic = ChatTopic(name=name, user_id=current_user.id)
    session.add(topic)
    session.commit()
    session.refresh(topic)
    
    return topic

@router.get("/chat/topics")
async def get_user_topics(
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
) -> Sequence[ChatTopic]:
    
    topics = session.exec(
        select(ChatTopic)
        .where(ChatTopic.user_id == current_user.id)
    ).all()
    
    return topics

@router.get("/chat/messages")
async def get_messages_by_topic(
    topic_id : int,
    session: SessionDep,
    current_user: UserBase = Depends(get_current_active_user)
):
    chat = session.exec(
        select(Chat)
        .where(
            Chat.topic_id == topic_id and
            Chat.user_id == current_user.id
        )
        .order_by(Chat.created_at.asc())
        ).all()
    
    return chat

@router.get("/chat/topics")
async def get_single_topic(
    topic_id : int,
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
):
    topic = session.exec(
        select(ChatTopic)
        .where(ChatTopic.user_id == current_user.id and 
               ChatTopic.id == topic_id)
        ).one_or_none()
    
    return topic