from sqlalchemy.ext.asyncio import AsyncSession
from models.notification import Notification
from repositories.notification_repository import NotificationRepository

class NotificationService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, user_id: int, title: str, message: str, channel: str = "in_app"):
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            channel=channel,
        )
        return await NotificationRepository.create(self.db, notification)

    async def get_all_notifications(self, user_id: int):
        return await NotificationRepository.get_by_user(self.db, user_id)


    async def get_notification(self, notification_id: int, user_id: int):
        return await NotificationRepository.get_one(self.db, notification_id, user_id)

    async def mark_as_read(self, notification_id: int, user_id: int):
        await NotificationRepository.mark_as_read(self.db, notification_id, user_id)

    async def clear_all(self, user_id: int):
        await NotificationRepository.clear_all(self.db, user_id)

    async def get_unread_notifications(self, user_id: int):
        notifications = await NotificationRepository.get_by_user(self.db, user_id)
        return [n for n in notifications if not n.is_read]
