"""add postal_code to services

Revision ID: c9f3e31b2a11
Revises: 503f9e41d077
Create Date: 2026-06-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9f3e31b2a11'
down_revision: Union[str, Sequence[str], None] = '503f9e41d077'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('services', sa.Column('postal_code', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('services', 'postal_code')
