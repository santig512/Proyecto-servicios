from datetime import datetime
from pydantic import BaseModel, Field


class LandingReviewCreate(BaseModel):
    author_name: str | None = Field(default=None, max_length=120)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=3, max_length=1200)


class LandingReviewRead(BaseModel):
    id: int
    author_name: str | None
    rating: int
    comment: str
    created_at: datetime | None

    model_config = {
        'from_attributes': True,
    }


class LandingReviewPage(BaseModel):
    items: list[LandingReviewRead]
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_prev: bool
    has_next: bool
