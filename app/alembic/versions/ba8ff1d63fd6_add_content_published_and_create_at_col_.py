"""add content, published and create_at col for posts table

Revision ID: ba8ff1d63fd6
Revises: a5aeabb39ad5
Create Date: 2023-05-09 15:25:04.026109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8ff1d63fd6'
down_revision = 'a5aeabb39ad5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('title',sa.String, nullable=False))
    op.add_column('posts', sa.Column('publisted', sa.Boolean, nullable=False,server_default="TRUE"))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text("now()")))


def downgrade() -> None:
    op.drop_column('title', "posts")
    op.drop_column('published', "posts")    
    op.drop_column('create_at', "posts")