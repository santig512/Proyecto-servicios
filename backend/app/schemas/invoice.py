from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvoiceCreate(BaseModel):
    service_id: int
    invoice_number: str
    amount: float
    payment_status: Optional[str] = "pending"
    payment_method: Optional[str] = None

class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = None
    amount: Optional[float] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None

class InvoiceRead(BaseModel):
    id: int
    service_id: int
    invoice_number: str
    amount: float
    payment_status: str
    payment_method: Optional[str]
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }
