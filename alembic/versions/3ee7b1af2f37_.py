"""empty message

Revision ID: 3ee7b1af2f37
Revises: 88c25b7147ea
Create Date: 2023-01-11 18:35:03.637312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ee7b1af2f37'
down_revision = '88c25b7147ea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('deep_link', sa.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'deep_link')
    # ### end Alembic commands ###