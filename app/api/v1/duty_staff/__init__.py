from fastapi import APIRouter
from .duty_staff import router

duty_staff_router = APIRouter()
duty_staff_router.include_router(router, tags=["勤务模块"])

__all__ = ["duty_staff_router"]
