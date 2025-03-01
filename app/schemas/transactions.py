from pydantic import BaseModel, Field
from datetime import datetime

class TransactionRecord(BaseModel):
    payment_time: datetime = Field(..., description="支付时间", example="2023-10-01T12:00:00")
    payment_amount: float = Field(..., description="支付金额", example=100.00)
    recipient: str = Field(..., description="收款人", example="张三")

class TransactionCreate(TransactionRecord):
    pass

class TransactionUpdate(TransactionRecord):
    id: int = Field(..., description="交易记录ID")