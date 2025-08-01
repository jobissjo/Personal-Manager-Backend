from app.core.logger_config import logger as default_logger
from app.models.user import User
from app.schemas import (
    HabitCategoryRequestSchema,
    HabitCategoryModelSchema,
    HabitCategoryResponseSchema,
    HabitCategoryPartialRequestSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import HabitCategoryRepository


class HabitCategoryService:
    def __init__(self, db: AsyncSession,logger=None):
        self.db = db
        self.logger = logger or default_logger

    async def get_all_habit_categories(
        self,
        name: str = None,
        search: str = None,
    ):
        return await HabitCategoryRepository(self.db).get_all_habit_categories(
            name=name, search=search
        )

    async def get_habit_category_by_id(self, category_id: int, db: AsyncSession):
        return await HabitCategoryRepository(db).get_habit_category_by_id(category_id)

    async def create_habit_category(
        self,
        category_data: HabitCategoryRequestSchema,
        current_user: User,
    ) -> HabitCategoryResponseSchema:
        habit_category_data = HabitCategoryModelSchema(
            **category_data.model_dump(), user_id=current_user.id
        )
        return await HabitCategoryRepository(self.db).create_habit_category(
            habit_category_data
        )

    async def update_habit_category_by_id(
        self,
        category_id: int,
        category_data: HabitCategoryPartialRequestSchema,
    ) -> HabitCategoryResponseSchema:
        return await HabitCategoryRepository(self.db).update_habit_category_by_id(
            category_id, category_data
        )

    async def delete_habit_category_by_id(
        self, category_id: int,
    ) -> HabitCategoryResponseSchema:
        return await HabitCategoryRepository(self.db).delete_habit_category_by_id(
            category_id
        )
