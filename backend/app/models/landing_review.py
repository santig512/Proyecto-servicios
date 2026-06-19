from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.models.base import Base


class LandingReview(Base):
    __tablename__ = 'landing_reviews'

    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(120), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
