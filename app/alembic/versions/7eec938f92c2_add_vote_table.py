"""add vote table

Revision ID: 7eec938f92c2
Revises: ba8ff1d63fd6
Create Date: 2023-05-09 15:47:21.499582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eec938f92c2'
down_revision = 'ba8ff1d63fd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], onupdate='NO ACTION', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.drop_column('posts', 'publisted')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.add_column('posts', sa.Column('publisted', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_column('posts', 'published')
    op.drop_table('votes')
    # ### end Alembic commands ###
