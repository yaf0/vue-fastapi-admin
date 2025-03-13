from pydantic import BaseModel, Field
from datetime import datetime

class DutyStaffBase(BaseModel):
    name: str= Field(..., description="勤务人员名称")
    type: str = Field(..., description="勤务人员类型")

class DutyStaffCreate(DutyStaffBase):
    pass

class DutyStaffUpdate(DutyStaffBase):
    id: int = Field(..., description="勤务人员ID")
    actual_expenditure: int = Field(..., description="实际支出")


