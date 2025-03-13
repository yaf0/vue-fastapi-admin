from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FieldWorkRecordBase(BaseModel):
    name: str= Field(..., description="外勤名称")
    number: int = Field(..., description="台数")
    expected_expenditure: int = Field(..., description="预期支出")
    difference: int = Field(..., description="差额")
    date: datetime = Field(..., description="日期")
    remark: Optional[str] = Field(None, description="备注")

class FieldWorkRecordCreate(FieldWorkRecordBase):
    pass

class FieldWorkRecordUpdate(FieldWorkRecordBase):
    id: int = Field(..., description="记录ID")
