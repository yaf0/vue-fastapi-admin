from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.controllers.duty_staff import duty_staff_controller
from app.controllers.total import total_record_yyfs_controller
from app.schemas import Success, SuccessExtra
from app.schemas.duty_staff import DutyStaffCreate, DutyStaffUpdate

router = APIRouter()


@router.get("/list", summary="查看勤务人员列表")
async def list_duty_staffs(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query(None, description="人员名称"),
    type: str = Query(None, description="人员类型"),
):
    q = Q()
    if name:
        q &= Q(name__contains=name)
    if type:
        q &= Q(type__contains=type)
    total, duty_staff_objs = await duty_staff_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in duty_staff_objs]

    # 获取每个外勤的台数总计和预期支出总计
    for item in data:
        if item.get('type') == '外勤人员':
            field_staff = item.get('name')
            if field_staff:
                q_yyfs = Q(field_staff__contains=field_staff)
                _, total_objs_yyfs = await total_record_yyfs_controller.list(page=1, page_size=100000, search=q_yyfs)
                yyfs_data = [await obj.to_dict() for obj in total_objs_yyfs]
                item['count'] = len(yyfs_data)
                item['expected_expenditure_sum'] = sum(yyfs_item['expected_expenditure'] for yyfs_item in yyfs_data)

    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看单个勤务人员")
async def get_duty_staff_api(id: int = Query(..., description="勤务人员ID")):
    duty_staff_obj = await duty_staff_controller.get(id=id)
    data = await duty_staff_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="创建勤务人员")
async def create_duty_staff_api(duty_staff_in: DutyStaffCreate):
    duty_staff = await duty_staff_controller.create(obj_in=duty_staff_in)
    duty_staff_data = await duty_staff.to_dict()  # 转换为字典
    return Success(data=duty_staff_data)


@router.post("/update", summary="更新勤务人员")
async def update_duty_staff_api(duty_staff_in: DutyStaffUpdate):
    duty_staff = await duty_staff_controller.update(id=duty_staff_in.id, obj_in=duty_staff_in)
    duty_staff_data = await duty_staff.to_dict()  # 转换为字典
    return Success(data=duty_staff_data)


@router.delete("/delete", summary="删除勤务人员")
async def delete_duty_staff_api(id: int = Query(..., description="勤务人员ID")):
    await duty_staff_controller.remove(id=id)
    return Success(msg="Deleted Successfully")
