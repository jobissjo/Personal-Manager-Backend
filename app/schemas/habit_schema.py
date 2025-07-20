from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user_schema import UserBasicSchema
from app.schemas.habit_category_schema import HabitCategoryResponseSchema


class HabitRequestSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    category_id: int


class HabitPartialRequestSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category_id: Optional[int] = None


class HabitModelSchema(HabitRequestSchema):
    user_id: int


class HabitResponseSchema(HabitRequestSchema):
    id: int
    user_id: int
    user: UserBasicSchema
    category: HabitCategoryResponseSchema
