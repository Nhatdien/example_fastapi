"""add content column

Revision ID: 53c90de31c55
Revises: ebc09c652b98
Create Date: 2023-05-09 14:43:52.031062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53c90de31c55'
down_revision = 'ebc09c652b98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
