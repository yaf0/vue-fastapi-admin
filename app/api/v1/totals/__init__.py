from fastapi import APIRouter
from .totals import router

totals_router = APIRouter()
totals_router.include_router(router, tags=["总表模块"])

__all__ = ["totals_router"]

