"""create landing reviews

Revision ID: f2d8a1a0d7f4
Revises: c9f3e31b2a11
Create Date: 2026-06-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2d8a1a0d7f4'
down_revision: Union[str, Sequence[str], None] = 'c9f3e31b2a11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'landing_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author_name', sa.String(length=120), nullable=True),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_landing_reviews_id'), 'landing_reviews', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_landing_reviews_id'), table_name='landing_reviews')
    op.drop_table('landing_reviews')
