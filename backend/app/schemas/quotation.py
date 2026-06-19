from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuotationCreate(BaseModel):
    service_id: int
    amount: float
    description: Optional[str] = None

class QuotationUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    approved_by_customer: Optional[bool] = None

class QuotationRead(BaseModel):
    id: int
    service_id: int
    amount: float
    description: Optional[str]
    approved_by_customer: bool
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }
