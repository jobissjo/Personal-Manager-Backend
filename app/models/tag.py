# app/models/tag.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.core.db_config import Base
from typing import List
from app.models.association import note_tag_table

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.note import Note

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    notes: Mapped[List["Note"]] = relationship(
        "Note",
        secondary=note_tag_table,
        back_populates="tags"
    )
