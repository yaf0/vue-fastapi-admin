from fastapi import APIRouter
from .field_work import router

field_work_router = APIRouter()
field_work_router.include_router(router, tags=["外勤模块"])

__all__ = ["field_work_router"]

