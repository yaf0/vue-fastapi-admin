from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.controllers.total import total_record_controller, total_record_yyfs_controller, total_record_controller_bs
from app.controllers.user import user_controller
from app.schemas import Success, SuccessExtra
from app.schemas.total import TotalRecordCreate, TotalRecordUpdate

router = APIRouter()


@router.get("/list", summary="查看总表数据列表")
async def list_totals(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    date: str = Query(None, description="日期"),
    plate: str = Query(None, description="车牌"),
    business: str = Query(None, description="业务"),
    field_staff: str = Query(None, description="外勤"),
):
    q = Q()
    if date:
        q &= Q(date__contains=date)
    if plate:
        q &= Q(plate__contains=plate)
    if business:
        q &= Q(business__contains=business)
    if field_staff:
        q &= Q(field_staff__contains=field_staff)

    total, total_objs = await total_record_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in total_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

@router.get("/list/yy", summary="查看总表数据列表-yy专用")
async def list_totals(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    date: str = Query(None, description="日期"),
    plate: str = Query(None, description="车牌"),
    business: str = Query(None, description="业务"),
    field_staff: str = Query(None, description="外勤"),
):
    q = Q()
    if date:
        q &= Q(date__contains=date)
    if plate:
        q &= Q(plate__contains=plate)
    if business:
        q &= Q(business__contains=business)
    if field_staff:
        q &= Q(field_staff__contains=field_staff)

    total, total_objs = await total_record_controller.list(page=page, page_size=page_size, search=q)
    data = [
        {
            key: obj[key]
            for key in obj.keys()
            if key != "income"
        }
        for obj in [await obj.to_dict() for obj in total_objs]
    ]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

# @router.get("/list/yyfs", summary="查看外勤数据列表yy外勤")
# async def list_totals_yyfs(
#     page: int = Query(1, description="页码"),
#     page_size: int = Query(10, description="每页数量"),
#     field_staff: str = Query(None, description="外勤"),
# ):
#     q = Q()
#     if field_staff:
#         q &= Q(field_staff__contains=field_staff)

#     total, total_objs = await total_record_yyfs_controller.list(page=page, page_size=page_size, search=q)
#     data = [await obj.to_dict() for obj in total_objs]

#     # 统计字段
#     count = len(data)
#     expected_expenditure_sum = sum(item['expected_expenditure'] for item in data)

#     return SuccessExtra(data=data, total=total, page=page, page_size=page_size, count=count, expected_expenditure_sum=expected_expenditure_sum)

@router.get("/list/bs", summary="查看业务员维度数据列表")
async def list_totals_bs(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    business: str = Query(None, description="业务"),
):
    total_count = 0
    total_expected_expenditure_sum = 0
    total_income_sum = 0

    q = Q()
    if business:
        q &= Q(business__contains=business)

        total, total_objs = await total_record_controller_bs.list(page=1, page_size=9999, search=q)
        business_data = [await obj.to_dict() for obj in total_objs]
        data = [{
            'business': business,
            'count': total,
            'expected_expenditure': sum(item['expected_expenditure'] for item in business_data),
            'income': sum(item['income'] for item in business_data),
        }]

        total_count = data[0]['count']
        total_expected_expenditure_sum = data[0]['expected_expenditure']
        total_income_sum = data[0]['income']
        
    else:
        total_business = await user_controller.list(page=page, page_size=page_size)
        business_list = [item.username for item in total_business[1] if item.dept_id == 5]
        data = []

        for business in business_list:
            q = Q(business=business)
            _, total_objs = await total_record_controller_bs.list(page=1, page_size=9999, search=q)
            business_data = [await obj.to_dict() for obj in total_objs]
            data.append({
                'business': business,
                'count': len(business_data),
                'expected_expenditure': sum(item['expected_expenditure'] for item in business_data),
                'income': sum(item['income'] for item in business_data),
            })

        total_count = sum(item['count'] for item in data)
        total_expected_expenditure_sum = sum(item['expected_expenditure'] for item in data)
        total_income_sum = sum(item['income'] for item in data)

    return SuccessExtra(data=data, total=len(data), page=page, page_size=page_size, count_sum=total_count, expected_expenditure_sum=total_expected_expenditure_sum, income_sum=total_income_sum)

@router.get("/get", summary="查看单条总表数据")
async def get_total(id: int = Query(..., description="记录ID")):
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
async def delete_total(id: int = Query(..., description="记录ID")):
    await total_record_controller.remove(id=id)
    return Success(msg="Deleted Successfully")

@router.get("/list/ob", summary="查看我的数据列表")
async def list_totals(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    date: str = Query(None, description="日期"),
    plate: str = Query(None, description="车牌"),
    business: str = Query(None, description="业务"),
    docking_time_not_null: bool = Query(False, description="是否对接"),
    is_completed: bool = Query(None, description="是否完成"),
):
    q = Q()
    if date:
        q &= Q(date__contains=date)
    if plate:
        q &= Q(plate__contains=plate)
    if business:
        q &= Q(business__contains=business)
    if docking_time_not_null:
        q &= Q(docking_time__not_isnull=True)
    if is_completed is not None:
        q &= Q(is_completed=is_completed)

    total, total_objs = await total_record_controller.list(page=page, page_size=page_size, search=q)
    data = [
        {
            "id": obj["id"],
            "date": obj["date"],
            "plate": obj["plate"],
            "region": obj["region"],
            "company": obj["company"],
            "business": obj["business"],
            "income": obj["income"],
            "remark": obj["remark"],
            "docking_time": obj["docking_time"],
            "handover_time": obj["handover_time"],
            "is_completed": obj["is_completed"],
        }
        for obj in [await obj.to_dict() for obj in total_objs]
    ]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

@router.post("/update/ob", summary="更新我的数据")
async def update_total(total_in: TotalRecordUpdate):
    await total_record_controller.update(id=total_in.id, obj_in=total_in)
    return Success(msg="Updated Successfully")
