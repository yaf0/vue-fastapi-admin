from fastapi import APIRouter
from .totals import router

totals_router = APIRouter()
totals_router.include_router(router, tags=["外勤模块"])

__all__ = ["field_work_router"]

