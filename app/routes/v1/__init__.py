from fastapi import APIRouter
from app.routes.v1 import (
    auth_routes,
    user_routes,
    reminder_routes,
    habit_routes,
    habit_category_routes,
    note_routes,
    notification_routes,
    google_keep_routes,
)

router = APIRouter()
router.include_router(auth_routes.router)
router.include_router(user_routes.router)
router.include_router(reminder_routes.router)
router.include_router(habit_routes.router)
router.include_router(habit_category_routes.router)
router.include_router(note_routes.router)
router.include_router(notification_routes.router)
router.include_router(google_keep_routes.router)
