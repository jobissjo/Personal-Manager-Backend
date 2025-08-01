from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification_schema import NotificationCreate, NotificationRead

class NotificationService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, user_id: int, data: NotificationCreate)->NotificationRead:
        notification = Notification(
            user_id=user_id,
            title=data.title,
            message=data.message,
            channel=data.channel,
        )
        return await NotificationRepository.create(self.db, notification)

    async def get_all_notifications(self, user_id: int)->List[NotificationRead]:
        return await NotificationRepository.get_by_user(self.db, user_id)


    async def get_notification(self, notification_id: int, user_id: int)->NotificationRead:
        return await NotificationRepository.get_one(self.db, notification_id, user_id)

    async def mark_as_read(self, notification_id: int, user_id: int)->None:
        await NotificationRepository.mark_as_read(self.db, notification_id, user_id)

    async def clear_all(self, user_id: int)->None:
        await NotificationRepository.clear_all(self.db, user_id)

    async def get_unread_notifications(self, user_id: int):
        notifications = await NotificationRepository.get_by_user(self.db, user_id, is_read=False)
        return notifications
