from pydantic import BaseModel, Field
from app.schemas.user_schema import UserBasicSchema
from typing import Optional


class HabitCategoryRequestSchema(BaseModel):
    name: str = Field(max_length=50)
    icon_name: str = Field(max_length=50, alias="iconName", description="Icon name for the habit category")

class HabitCategoryModelSchema(HabitCategoryRequestSchema):
    user_id: int

class HabitCategoryResponseSchema(HabitCategoryRequestSchema):
    id: int
    user_id: int
    user: UserBasicSchema

class HabitCategoryPartialRequestSchema(BaseModel):  # for PATCH
    name: Optional[str] = Field(None, max_length=50)
    icon_name: Optional[str] = Field(None, max_length=50, alias="iconName")