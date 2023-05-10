"""create post table

Revision ID: ebc09c652b98
Revises: 
Create Date: 2023-05-08 20:56:45.213367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebc09c652b98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column("id", sa.Integer, nullable=False, primary_key=True))


def downgrade() -> None:
    op.drop_table('posts')
