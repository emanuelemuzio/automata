from fastapi import APIRouter
from typing import Annotated, Sequence
from fastapi import Depends, APIRouter
from ..service.auth import *
from ..service.chat import *
from ..request.ChatRequest import ChatRequest
from ..response.ChatResponse import ChatResponse

router = APIRouter()

@router.put("/chat", tags=['Chat'], description="Route for posing a question to Automata")
async def pose_chat_question(
    session: SessionDep,
    request : ChatRequest,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):

    response = invoke_automata(request.question, request.topic_id, current_user, session) 
    return response

@router.get("/chat", tags=['Chat'], description="Route for retrieving a topic message history in chronological order")
async def get_topic_messages(
    topic_id : int,
    session: SessionDep,
    current_user: UserBase = Depends(get_current_active_user)
) -> Sequence[Chat]:
    
    response = retrieve_chat_history(topic_id, current_user.id, session)
    return response