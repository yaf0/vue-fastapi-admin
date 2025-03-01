from fastapi import APIRouter

from .transactions import router

transactions_router = APIRouter()
transactions_router.include_router(router, tags=["CURD"])

__all__ = ["transactions_router"]
