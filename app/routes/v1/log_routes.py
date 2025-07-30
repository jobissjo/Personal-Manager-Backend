from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_config import get_db
from app.core.permissions import any_user_role
from app.models.user import User
from app.services.log_service import LogService
from app.schemas.common_schema import BaseResponse
from app.schemas.log_schema import LogCreate, LogRead


router = APIRouter(prefix="/logs", tags=["Logs"])

def get_log_service(db: AsyncSession = Depends(get_db)):
    from app.services.log_service import LogService
    return LogService(db)

@router.post("/", response_model=BaseResponse[LogRead])
async def create_log(
    log_data: LogCreate,
    current_user: User = Depends(any_user_role),
    service: LogService = Depends(get_log_service)
):
    log_data['user_id'] = current_user.id
    log_entry = await service.create_log(log_data)
    return BaseResponse(message="Log created successfully", data=log_entry)


@router.get("/", response_model=BaseResponse[list[LogRead]])
async def get_user_logs(
    current_user: User = Depends(any_user_role),
    service: LogService = Depends(get_log_service)
):
    logs = await service.get_user_logs(current_user.id)
    return BaseResponse(message="User logs fetched successfully", data=logs)


