"""empty message

Revision ID: 79ef435f2696
Revises: 
Create Date: 2023-01-09 00:18:08.124395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79ef435f2696'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=255), nullable=False),
    sa.Column('question', sa.VARCHAR(length=3000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('telegram_id', sa.BIGINT(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=255), nullable=True),
    sa.Column('full_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('language_code', sa.VARCHAR(length=10), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('reflection_time', sa.Integer(), server_default='19', nullable=True),
    sa.Column('referrer_id', sa.BIGINT(), nullable=True),
    sa.ForeignKeyConstraint(['referrer_id'], ['users.telegram_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    op.create_table('answers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('telegram_id', sa.BIGINT(), nullable=False),
    sa.Column('question_id', sa.BIGINT(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=255), nullable=False),
    sa.Column('answer', sa.VARCHAR(length=3000), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['telegram_id'], ['users.telegram_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    op.drop_table('users')
    op.drop_table('questions')
    # ### end Alembic commands ###
