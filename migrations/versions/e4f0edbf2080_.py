"""empty message

Revision ID: e4f0edbf2080
Revises: 
Create Date: 2024-03-25 12:34:37.449599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f0edbf2080'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('tbl_ruhsat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('yapi_yuksekligi', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('zemin_alti_kat_sayisi', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('zemin_ustu_kat_sayisi', sa.Integer(), nullable=True))

