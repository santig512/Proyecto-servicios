"""create services table for public requests

Revision ID: 0002_create_services_public_requests
Revises: 0001_create_users
Create Date: 2026-05-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql

# revision identifiers, used by Alembic.
revision = '0002_create_services_public_requests'
down_revision = '0001_create_users'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'services',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('assigned_technician_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('customer_name', sa.String(), nullable=True),
        sa.Column('customer_email', sa.String(), nullable=True),
        sa.Column('customer_phone', sa.String(), nullable=True),
        sa.Column('service_address', sa.String(), nullable=True),
        sa.Column('tracking_code', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(), nullable=False, server_default='normal'),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('scheduled_date', sa.DateTime(timezone=False), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
        sa.Column('final_cost', sa.Float(), nullable=True),
        sa.Column('address_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table('services')
