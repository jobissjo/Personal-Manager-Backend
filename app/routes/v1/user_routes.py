from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.core.db_config import get_db
from app.core.permissions import any_user_role
from app.models import User
from app.schemas.common_schema import BaseResponse
from app.schemas.user_schema import ProfileUpdateSchema, ProfileUpdateForm, UserBasicSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import EmailService, UserService


router = APIRouter(prefix="/user", tags=["User"])


def get_email_service() -> EmailService:
    return EmailService()


def get_user_service(
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
) -> UserService:
    return UserService(email_service=email_service, db=db)


@router.get(
    "/",
    response_model=UserBasicSchema,
    summary="Get current user profile",
    description="Returns the profile information of the currently authenticated user"
)
async def get_user_profile(user: Annotated[User, Depends(any_user_role)]) -> UserBasicSchema:
    return user


@router.patch(
    "/",
    response_model=BaseResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Update user profile",
    description="Update the current user's profile information"
)
async def update_profile(
    data: ProfileUpdateSchema,
    current_user: Annotated[User, Depends(any_user_role)],
    service: Annotated[UserService, Depends(get_user_service)]
) -> BaseResponse[None]:
    await service.update_profile(current_user.id, data)
    return BaseResponse(message="Profile updated successfully", data=None)


@router.patch(
    "/form-data",
    response_model=BaseResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Update user profile with form data",
    description="Update the current user's profile information using form data"
)
async def update_profile_with_form(
    form_data: Annotated[ProfileUpdateForm, Depends()],
    current_user: Annotated[User, Depends(any_user_role)],
    service: Annotated[UserService, Depends(get_user_service)]
) -> BaseResponse[None]:
    await service.update_profile_form(current_user.id, form_data)
    return BaseResponse(message="Profile updated successfully", data=None)