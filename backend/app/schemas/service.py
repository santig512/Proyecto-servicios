from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServiceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    service_address: Optional[str] = None
    postal_code: Optional[str] = None
    category_id: Optional[int] = None
    address_id: Optional[int] = None
    scheduled_date: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    customer_id: Optional[int] = None


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    service_address: Optional[str] = None
    postal_code: Optional[str] = None
    category_id: Optional[int] = None
    address_id: Optional[int] = None
    scheduled_date: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    final_cost: Optional[float] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_technician_id: Optional[int] = None

class ServiceRead(BaseModel):
    id: int
    customer_id: Optional[int]
    assigned_technician_id: Optional[int]
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    service_address: Optional[str]
    postal_code: Optional[str]
    tracking_code: str
    category_id: Optional[int]
    title: str
    description: Optional[str]
    priority: str
    status: str
    scheduled_date: Optional[datetime]
    estimated_cost: Optional[float]
    final_cost: Optional[float]
    address_id: Optional[int]
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }
