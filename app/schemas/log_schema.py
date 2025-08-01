from pydantic import BaseModel, Field
from typing import Optional, List

from app.schemas.user_schema import UserBasicSchema

class LogCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user creating the log")
    action: str = Field(..., description="Action performed by the user")
    message: Optional[str] = Field(None, description="Optional message for the log")
    note_id: Optional[int] = Field(None, description="ID of the associated note", alias="noteId")
    reminder_id: Optional[int] = Field(None, description="ID of the associated reminder", alias="reminderId")
    habit_id: Optional[int] = Field(None, description="ID of the associated habit", alias="habitId")


class LogRead(LogCreate):
    id: int = Field(..., description="Unique identifier of the log")
    timestamp: str = Field(..., description="Timestamp when the log was created", alias="createdAt")
    user: Optional[UserBasicSchema] = Field(None, description="Username of the user who created the log", alias="userName")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True