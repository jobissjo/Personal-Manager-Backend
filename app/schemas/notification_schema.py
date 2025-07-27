from pydantic import BaseModel, Field
from typing import Optional, List

class NotificationCreate(BaseModel):
    title: str = Field(..., description="Title of the notification")
    message: str = Field(..., description="Content of the notification")
    channel: Optional[str] = Field("in_app", description="Channel through which the notification is sent")
    type: Optional[str] = Field("info", description="Type of notification, e.g., 'info', 'job_alert', 'reminder'")

class NotificationRead(NotificationCreate):
    id: int = Field(..., description="Unique identifier of the notification")
    is_read: bool = Field(False, description="Indicates if the notification has been read", alias="read")
    sent: bool = Field(False, description="Indicates if the notification has been sent")
    created_at: str = Field(..., description="Timestamp when the notification was created", alias="createdAt")
    updated_at: str = Field(..., description="Timestamp when the notification was last updated", alias="updatedAt")

    class Config:
        from_attributes = True
