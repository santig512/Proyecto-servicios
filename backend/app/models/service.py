from uuid import uuid4

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from app.models.base import Base

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    assigned_technician_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    customer_phone = Column(String, nullable=True)
    service_address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    tracking_code = Column(String, unique=True, index=True, nullable=False, default=lambda: uuid4().hex[:10].upper())
    category_id = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default='normal')
    status = Column(String, default='pending')
    scheduled_date = Column(DateTime, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    final_cost = Column(Float, nullable=True)
    address_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
