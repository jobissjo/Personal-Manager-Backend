from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from sqlalchemy import DateTime, Integer, String, func, ForeignKey, Enum, Date
from typing import TYPE_CHECKING, List
from app.models.enums import FrequencyType

if TYPE_CHECKING:
    from app.models.common import HabitCategory
    from app.models.user import User
    from app.models.log import Log


class Habit(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("habit_categories.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped["HabitCategory"] = relationship(
        "HabitCategory", back_populates="habits"
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="habits")

    frequency_type: Mapped[FrequencyType] = mapped_column(
        Enum(FrequencyType), nullable=False
    )
    frequency_count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    logs: Mapped[List["HabitLog"]] = relationship(
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )
    system_logs: Mapped[List["Log"]] = relationship(
        "Log", back_populates="habit", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Habit(id={self.id}, title={self.title}, category_id={self.category_id}, user_id={self.user_id})>"


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"), nullable=False
    )
    completed_date: Mapped[date] = mapped_column(
        Date, nullable=False, index=True
    )  # The date user marks habit as done
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    habit: Mapped["Habit"] = relationship("Habit", back_populates="logs")

    def __repr__(self):
        return f"<HabitLog(id={self.id}, habit_id={self.habit_id}, date={self.date})>"
