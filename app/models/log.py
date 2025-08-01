from app.core.db_config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, Text
from typing import  TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.habit import Habit
    from app.models.note import Note
    from app.models.reminder import Reminder


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="logs")
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), nullable=True)
    habit: Mapped["Habit"] = relationship("Habit", back_populates="system_logs", )
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"), nullable=True)
    note: Mapped["Note"] = relationship("Note", back_populates="logs", )
    reminder_id: Mapped[int] = mapped_column(ForeignKey("reminders.id", ondelete="CASCADE"), nullable=True)
    reminder: Mapped["Reminder"] = relationship("Reminder", back_populates="logs", )

    action: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[Text] = mapped_column(Text, nullable=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), index=True)

    def __repr__(self):
        return f"<Log(id={self.id}, user_id={self.user_id}, action={self.action}, timestamp={self.timestamp})>"