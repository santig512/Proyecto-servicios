from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    invoice_id: int
    transaction_reference: Optional[str] = None
    amount: float
    status: Optional[str] = "pending"
    provider: Optional[str] = None

class PaymentUpdate(BaseModel):
    transaction_reference: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    provider: Optional[str] = None
    paid_at: Optional[datetime] = None

class PaymentRead(BaseModel):
    id: int
    invoice_id: int
    transaction_reference: Optional[str]
    amount: float
    status: str
    provider: Optional[str]
    paid_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }
