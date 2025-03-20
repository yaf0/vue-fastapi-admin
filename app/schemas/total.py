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
    account: str = Field(..., description="账号")
    password: str = Field(..., description="密码")
    business: str = Field(..., description="业务")
    expected_expenditure: int = Field(..., description="预期支出")
    income: Optional[int] = Field(0, description="收入")
    destination: str = Field(..., description="去向")
    remark: Optional[str] = Field(None, description="备注")
    docking_time: Optional[datetime] = Field(None, description="对接时间")
    handover_time: Optional[datetime] = Field(None, description="交接时间") 
    is_completed: Optional[bool] = Field(None, description="是否完成")

class TotalRecordCreate(TotalRecordBase):
    pass

class TotalRecordUpdate(BaseModel):
    id: int = Field(..., description="记录ID")
    date: Optional[datetime] = Field(None, description="日期")
    plate: Optional[str] = Field(None, description="车牌")
    region: Optional[str] = Field(None, description="区域")
    company: Optional[str] = Field(None, description="公司")
    field_staff: Optional[str] = Field(None, description="外勤")
    internal_staff: Optional[str] = Field(None, description="内勤")
    platform: Optional[str] = Field(None, description="平台")
    account: Optional[str] = Field(None, description="账号")
    password: Optional[str] = Field(None, description="密码")
    business: Optional[str] = Field(None, description="业务")
    expected_expenditure: Optional[int] = Field(None, description="预期支出")
    income: Optional[int] = Field(None, description="收入")
    destination: Optional[str] = Field(None, description="去向")
    remark: Optional[str] = Field(None, description="备注")
    docking_time: Optional[datetime] = Field(None, description="对接时间")
    handover_time: Optional[datetime] = Field(None, description="交接时间")
    is_completed: Optional[bool] = Field(None, description="是否完成")

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

class TotalRecordBs(BaseModel):
    id: int = Field(..., description="记录ID")
    business: str = Field(..., description="业务")
    expected_expenditure: int = Field(..., description="预期支出")
    income: int = Field(..., description="收入")
    
class TotalRecordBsCreate(TotalRecordBs):
    pass

class TotalRecordBsUpdate(BaseModel):
    id: int
    business: Optional[str] = None
    expected_expenditure: Optional[int] = None
    income: Optional[int] = None
