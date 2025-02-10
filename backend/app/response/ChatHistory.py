from pydantic import BaseModel
from typing import Sequence
from ..common.Topic import Topic
from ..model.Chat import Chat

class ChatHistory(BaseModel):
    topic : Topic
    history : Sequence[Chat]