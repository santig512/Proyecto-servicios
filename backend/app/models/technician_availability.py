from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from app.models.base import Base

class TechnicianAvailability(Base):
    __tablename__ = 'technician_availability'

    id = Column(Integer, primary_key=True, index=True)
    technician_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    available_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
