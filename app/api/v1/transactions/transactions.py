from fastapi import APIRouter, Query
from tortoise.expressions import Q
from datetime import datetime

from app.controllers.transaction import api_controller
from app.schemas import Success, SuccessExtra
from app.schemas.transactions import *

router = APIRouter()

@router.get("/list", summary="查看交易记录列表")
async def list_transactions(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    payment_time: datetime = Query(None, description="支付时间"),
    payment_amount: float = Query(None, description="支付金额"),
    recipient: str = Query(None, description="收款人"),
):
    q = Q()
    if payment_time:
        q &= Q(payment_time__contains=payment_time)
    if payment_amount:
        q &= Q(payment_amount__contains=payment_amount)
    if recipient:
        q &= Q(recipient__contains=recipient)
    total, transaction_objs = await api_controller.list(page=page, page_size=page_size, search=q, order=["payment_time", "id"])
    data = [await obj.to_dict() for obj in transaction_objs]
    data = [{**transaction, 'payment_amount': float(transaction['payment_amount'])} for transaction in data]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

@router.get("/get", summary="查看交易记录")
async def get_transaction(
    id: int = Query(..., description="交易记录ID"),
):
    transaction_obj = await api_controller.get(id=id)
    data = await transaction_obj.to_dict()
    return Success(data=data)

@router.post("/create", summary="创建交易记录")
async def create_transaction(
    transaction_in: TransactionCreate,
):
    await api_controller.create(obj_in=transaction_in)
    return Success(msg="Created Successfully")

@router.post("/update", summary="更新交易记录")
async def update_transaction(
    transaction_in: TransactionUpdate,
):
    await api_controller.update(id=transaction_in.id, obj_in=transaction_in)
    return Success(msg="Update Successfully")

@router.delete("/delete", summary="删除交易记录")
async def delete_transaction(
    transaction_id: int = Query(..., description="交易记录ID"),
):
    await api_controller.remove(id=transaction_id)
    return Success(msg="Deleted Successfully")