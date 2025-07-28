from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.note import Note
from app.models.tag import Tag
from app.schemas.note_schema import NoteCreate, NoteUpdate

class NoteRepository:
    @staticmethod
    async def get_all(db: AsyncSession, user_id: int):
        result = await db.execute(select(Note).filter(Note.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def get(db: AsyncSession, note_id: int, user_id: int):
        result = await db.execute(select(Note).filter(Note.id == note_id, Note.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, note_data: NoteCreate, user_id: int):
        tags = []
        if note_data.tag_ids:
            tags = await db.execute(select(Tag).filter(Tag.id.in_(note_data.tag_ids)))
            tags = tags.scalars().all()

        note = Note(title=note_data.title, description=note_data.description, user_id=user_id, tags=tags)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    @staticmethod
    async def update(db: AsyncSession, note: Note, note_data: NoteUpdate):
        note.title = note_data.title
        note.description = note_data.description
        if note_data.tag_ids is not None:
            tags = await db.execute(select(Tag).filter(Tag.id.in_(note_data.tag_ids)))
            note.tags = tags.scalars().all()
        await db.commit()
        await db.refresh(note)
        return note

    @staticmethod
    async def delete(db: AsyncSession, note: Note):
        await db.delete(note)
        await db.commit()