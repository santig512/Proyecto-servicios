import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.landing_review import LandingReview
from app.schemas.review import LandingReviewCreate, LandingReviewPage, LandingReviewRead

router = APIRouter()

PAGE_SIZE = 10


@router.get('/public', response_model=LandingReviewPage)
async def list_public_reviews(
    page: int = Query(default=1, ge=1),
    db: AsyncSession = Depends(get_db),
):
    total_items_stmt = select(func.count()).select_from(LandingReview)
    total_items = (await db.execute(total_items_stmt)).scalar_one()
    total_pages = math.ceil(total_items / PAGE_SIZE) if total_items else 0

    current_page = min(page, total_pages) if total_pages else 1
    offset = (current_page - 1) * PAGE_SIZE

    reviews_stmt = (
        select(LandingReview)
        .order_by(LandingReview.created_at.desc(), LandingReview.id.desc())
        .offset(offset)
        .limit(PAGE_SIZE)
    )
    items = (await db.execute(reviews_stmt)).scalars().all()

    return {
        'items': [LandingReviewRead.model_validate(item) for item in items],
        'page': current_page,
        'page_size': PAGE_SIZE,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_prev': current_page > 1,
        'has_next': total_pages > 0 and current_page < total_pages,
    }


@router.post('/public', response_model=LandingReviewRead)
async def create_public_review(payload: LandingReviewCreate, db: AsyncSession = Depends(get_db)):
    author_name = (payload.author_name or '').strip() or None
    rating = int(payload.rating)
    review = LandingReview(
        author_name=author_name,
        rating=rating,
        comment=payload.comment.strip(),
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return LandingReviewRead.model_validate(review)
