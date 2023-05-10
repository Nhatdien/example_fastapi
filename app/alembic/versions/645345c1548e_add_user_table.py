"""add user table

Revision ID: 645345c1548e
Revises: 53c90de31c55
Create Date: 2023-05-09 14:54:13.568022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '645345c1548e'
down_revision = '53c90de31c55'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
