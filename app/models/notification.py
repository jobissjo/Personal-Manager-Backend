from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

IN_APP_NOTIFICATION = "in_app"
PUSH_NOTIFICATION = "push"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=True)

    type: Mapped[str] = mapped_column(String(50))  # e.g., 'info', 'job_alert', 'reminder'
    channel: Mapped[str] = mapped_column(String(50))  # 'in_app', 'push', 'email', etc.

    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    sent: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, title={self.title}, type={self.type}, channel={self.channel}, is_read={self.is_read})>"