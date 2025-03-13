from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TotalRecordBase(BaseModel):
    date: datetime = Field(..., description="日期")
    plate: str = Field(..., description="车牌")
    region: str = Field(..., description="区域")
    company: str = Field(..., description="公司")
    field_staff: str = Field(..., description="外勤")
    internal_staff: str = Field(..., description="内勤")
    platform: str = Field(..., description="平台")
    business: str = Field(..., description="业务")
    expected_expenditure: int = Field(..., description="预期支出")
    income: int = Field(..., description="收入")
    destination: str = Field(..., description="去向")
    remark: Optional[str] = Field(None, description="备注")
    handover_time: datetime = Field(..., description="交接时间")
    is_completed: bool = Field(..., description="是否完成")

class TotalRecordCreate(TotalRecordBase):
    pass

class TotalRecordUpdate(TotalRecordBase):
    id: int = Field(..., description="记录ID")
 
class TotalRecordYyfs(BaseModel):
    id: int = Field(..., description="记录ID")
    field_staff: str = Field(..., description="外勤")
    plate: str = Field(..., description="车牌")
    business: str = Field(..., description="业务")
    expected_expenditure: int = Field(..., description="预期支出")

class TotalRecordYyfsCreate(TotalRecordYyfs):
    pass

class TotalRecordYyfsUpdate(BaseModel):
    id: int
    field_staff: Optional[str] = None
    plate: Optional[str] = None
    business: Optional[str] = None
    expected_expenditure: Optional[float] = None
