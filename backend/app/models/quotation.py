from sqlalchemy import Column, Integer, ForeignKey, Float, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class Quotation(Base):
    __tablename__ = 'quotations'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    approved_by_customer = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
