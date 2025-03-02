from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.controllers.total import total_record_controller
from app.schemas import Success, SuccessExtra
from app.schemas.total import TotalRecordCreate, TotalRecordUpdate

router = APIRouter()

@router.get("/list", summary="查看总表数据列表")
async def list_totals(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    date: str = Query(None, description="日期"),
    plate: str = Query(None, description="车牌"),
    business: str = Query(None, description="业务")
):
    q = Q()
    if date:
        q &= Q(date__contains=date)
    if plate:
        q &= Q(plate__contains=plate)
    if business:
        q &= Q(business__contains=business)
    total, total_objs = await total_record_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in total_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

@router.get("/get", summary="查看单条总表数据")
async def get_total(
    id: int = Query(..., description="记录ID")
):
    total_obj = await total_record_controller.get(id=id)
    data = await total_obj.to_dict()
    return Success(data=data)

@router.post("/create", summary="创建总表数据")
async def create_total(total_in: TotalRecordCreate):
    await total_record_controller.create(obj_in=total_in)
    return Success(msg="Created Successfully")

@router.post("/update", summary="更新总表数据")
async def update_total(total_in: TotalRecordUpdate):
    await total_record_controller.update(id=total_in.id, obj_in=total_in)
    return Success(msg="Updated Successfully")

@router.delete("/delete", summary="删除总表数据")
async def delete_total(
    id: int = Query(..., description="记录ID")
):
    await total_record_controller.remove(id=id)
    return Success(msg="Deleted Successfully")

