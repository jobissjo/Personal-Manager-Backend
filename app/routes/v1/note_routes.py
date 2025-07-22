from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.permissions import any_user_role
from app.schemas.common_schema import BaseResponse
from app.schemas.note_schema import NoteCreate, NoteRead, NoteUpdate
from app.services.note_service import NoteService
from app.models.user import User
from app.core.db_config import get_db


def get_note_service(db: AsyncSession = Depends(get_db)) -> NoteService:
    return NoteService(db)

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/")
async def list_notes(
    current_user: User = Depends(any_user_role),
    service: NoteService = Depends(get_note_service)
)-> BaseResponse[List[NoteRead]]:
    response = await service.list_notes(current_user.id)
    return BaseResponse(message="Notes fetched successfully", data=response)

@router.post("/", response_model=NoteRead)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(any_user_role),
    service: NoteService = Depends(get_note_service)
):
    return await service.create_note(note_data, current_user.id)

@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    note_id: int,
    current_user: User = Depends(any_user_role),
    service: NoteService = Depends(get_note_service)
):
    note = await service.get_note(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(any_user_role),
    service: NoteService = Depends(get_note_service)
):
    updated = await service.update_note(note_id, current_user.id, note_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(any_user_role),
    service: NoteService = Depends(get_note_service)
):
    success = await service.delete_note(note_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
