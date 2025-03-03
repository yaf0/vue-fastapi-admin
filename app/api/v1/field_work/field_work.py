from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.controllers.field_work import field_work_record_controller
from app.schemas import Success, SuccessExtra
from app.schemas.field_work import FieldWorkRecordCreate, FieldWorkRecordUpdate

router = APIRouter()

@router.get("/list", summary="查看外勤数据列表")
async def list_field_works(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    date: str = Query(None, description="日期"),
    name: str = Query(None, description="外勤名称"),
):
    q = Q()
    if date:
        q &= Q(date__contains=date)
    if name:
        q &= Q(plate__contains=plate)
    field_work, field_work_objs = await field_work_record_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in field_work_objs]
    return SuccessExtra(data=data, field_work=field_work, page=page, page_size=page_size)

@router.get("/get", summary="查看单条外勤数据")
async def get_field_work(
    id: int = Query(..., description="记录ID")
):
    field_work_obj = await field_work_record_controller.get(id=id)
    data = await field_work_obj.to_dict()
    return Success(data=data)

@router.post("/create", summary="创建外勤数据")
async def create_field_work(field_work_in: FieldWorkRecordCreate):
    await field_work_record_controller.create(obj_in=field_work_in)
    return Success(msg="Created Successfully")

@router.post("/update", summary="更新外勤数据")
async def update_field_work(field_work_in: FieldWorkRecordUpdate):
    await field_work_record_controller.update(id=field_work_in.id, obj_in=field_work_in)
    return Success(msg="Updated Successfully")

@router.delete("/delete", summary="删除外勤数据")
async def delete_field_work(
    id: int = Query(..., description="记录ID")
):
    await field_work_record_controller.remove(id=id)
    return Success(msg="Deleted Successfully")

