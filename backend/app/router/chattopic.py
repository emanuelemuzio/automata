from fastapi import APIRouter
from typing import Sequence
from fastapi import Depends, APIRouter 
from ..service import chattopic as chat_topic_service
from ..service.auth import * 
from ..request.ChatTopicCreate import ChatTopicCreate 
from ..model.ChatTopic import ChatTopic

router = APIRouter() 
    
@router.put("/topic", tags=['Topic'], description="Route for creating a chat topic")
async def create_chat_topic(
    request : ChatTopicCreate, 
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
):
    
    chat_topic_service.create_chat_topic(request.name, current_user.id, session)
    return 

@router.get("/topic/by_user", tags=['Topic'], description="Route for getting the list of user topics")
async def get_user_topics(
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
) -> Sequence[ChatTopic]:
    
    response = chat_topic_service.get_user_topics(current_user.id, session)
    return response

@router.get("/topic", tags=['Topic'], description="Route for getting info about a single topic")
async def get_single_topic(
    idx : int,
    session: SessionDep, 
    _: UserBase = Depends(get_current_active_user)
):
    
    response = chat_topic_service.get_topic(idx, session)
    return response