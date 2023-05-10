"""add forign key to post table

Revision ID: a5aeabb39ad5
Revises: 645345c1548e
Create Date: 2023-05-09 15:06:44.142390

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'a5aeabb39ad5'
down_revision = '645345c1548e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer,
                                     sa.ForeignKey("users.id", ondelete="CASCADE",
                                                    onupdate="NO ACTION"), nullable=False)
                  )  

def downgrade() -> None:
    op.drop_constraint("posts_owner_id_fkey", table_name="posts")
    op.drop_column("post", "owner_id")
