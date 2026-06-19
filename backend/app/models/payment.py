from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    transaction_reference = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(String, default='pending')
    provider = Column(String, nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
