from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.user_schema import UserBasicSchema

class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None
    tag_ids: Optional[List[int]] = []

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    user_id: int
    tag_ids: List[int]
    user: UserBasicSchema
    created_at :str = Field(alias="createdAt")
    updated_at :str = Field(alias="updatedAt")

    class Config:
        from_attributes = True