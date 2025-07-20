from sqlalchemy import Table, Column, ForeignKey, Integer
from app.core.db_config import Base

note_tag_table = Table(
    "note_tag",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
