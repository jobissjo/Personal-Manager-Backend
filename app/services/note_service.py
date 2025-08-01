from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.note_schema import NoteCreate, NoteUpdate, NoteRead
from app.repositories.note_repositories import NoteRepository
from typing import List

from app.services.interface import INoteService


class NoteService(INoteService):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_notes(self, user_id: int) -> List[NoteRead]:
        return await NoteRepository.get_all(self.db, user_id)

    async def get_note(self, note_id: int, user_id: int):
        return await NoteRepository.get(self.db, note_id, user_id)

    async def create_note(self, note_data: NoteCreate, user_id: int):
        return await NoteRepository.create(self.db, note_data, user_id)

    async def update_note(self, note_id: int, user_id: int, note_data: NoteUpdate):
        note = await self.get_note(note_id, user_id)
        if not note:
            return None
        return await NoteRepository.update(self.db, note, note_data)

    async def delete_note(self, note_id: int, user_id: int):
        note = await self.get_note(note_id, user_id)
        if not note:
            return None
        await NoteRepository.delete(self.db, note)
        return True
