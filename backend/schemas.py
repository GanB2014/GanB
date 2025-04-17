from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CommentCreate(BaseModel):
    post_id: int
    content: str
    parent_id: Optional[int] = None
    user_id: str
    nickname: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    created_at: datetime
    user_id: int  # ✅ 수정 완료
    nickname: Optional[str] = None
    replies: Optional[List["CommentResponse"]] = []

    class Config:
        from_attributes = True

CommentResponse.update_forward_refs()

class CommentUpdate(BaseModel):
    content: str
    user_id: Optional[str] = None
    nickname: Optional[str] = None
