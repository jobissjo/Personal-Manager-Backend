from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.db_config import get_db
from app.models.user import User
from app.core.permissions import any_user_role, only_admin
from app.schemas import (
    HabitCategoryRequestSchema,
    BaseResponse,
    HabitCategoryResponseSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import HabitCategoryService

router = APIRouter(prefix="/habit-category", tags=["Auth"])
habit_service = HabitCategoryService()


@router.get("/")
async def create_habit_category(
    data: HabitCategoryRequestSchema,
    admin: Annotated[User, Depends(only_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BaseResponse[HabitCategoryResponseSchema]:
    data = await habit_service.create_habit_category(data, db, admin)
    return BaseResponse(message="Habit category created successfully", data=data)


@router.get("/")
async def get_all_habit_categories(
    db: Annotated[AsyncSession, Depends(get_db)], 
    user: Annotated[User, Depends(any_user_role)],
    name: str = None, search: str = None,

) -> BaseResponse[HabitCategoryResponseSchema]:
    data = await habit_service.get_all_habit_categories(db, name, search)
    return BaseResponse(message="Habit categories fetched successfully", data=data)


@router.get("/{category_id}")
async def get_habit_category_by_id(
    category_id: int, db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(any_user_role)],
) -> BaseResponse[HabitCategoryResponseSchema]:
    data = await habit_service.get_habit_category_by_id(category_id, db)
    return BaseResponse(message="Habit category fetched successfully", data=data)


@router.delete("/{category_id}")
async def delete_habit_category_by_id(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(only_admin)],
) -> BaseResponse[HabitCategoryResponseSchema]:
    data = await habit_service.delete_habit_category_by_id(category_id, db)
    return BaseResponse(message="Habit category deleted successfully", data=data)


@router.put("/{category_id}")
async def update_habit_category_by_id(
    category_id: int,
    data: HabitCategoryRequestSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(only_admin)],
) -> BaseResponse[HabitCategoryResponseSchema]:
    data = await habit_service.update_habit_category_by_id(category_id, data, db)
    return BaseResponse(message="Habit category updated successfully", data=data)


@router.patch("/{category_id}")
async def partial_update_habit_category_by_id(
    category_id: int,
    data: HabitCategoryRequestSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(only_admin)],
) -> BaseResponse[HabitCategoryResponseSchema]:
    data = await habit_service.update_habit_category_by_id(category_id, data, db)
    return BaseResponse(message="Habit category updated successfully", data=data)
