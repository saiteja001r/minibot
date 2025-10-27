from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    user_id: str
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    user_id: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
