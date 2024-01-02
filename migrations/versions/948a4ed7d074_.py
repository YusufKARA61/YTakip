"""empty message

Revision ID: 948a4ed7d074
Revises: 4817396a0cdb
Create Date: 2023-12-27 19:31:42.713966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '948a4ed7d074'
down_revision = '4817396a0cdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_projeler',
    sa.Column('proje_id', sa.Integer(), nullable=False),
    sa.Column('proje_adi', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('olusturma_tarihi', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['tbl_users.user_id'], ),
    sa.PrimaryKeyConstraint('proje_id')
    )
    op.create_table('tbl_veri',
    sa.Column('veri_id', sa.Integer(), nullable=False),
    sa.Column('proje_id', sa.Integer(), nullable=True),
    sa.Column('isim', sa.String(length=100), nullable=True),
    sa.Column('telefon', sa.String(length=15), nullable=True),
    sa.Column('tcno', sa.String(length=11), nullable=True),
    sa.Column('mvid', sa.Float(), nullable=True),
    sa.Column('kdsid', sa.Float(), nullable=True),
    sa.Column('arsaalan', sa.Float(), nullable=True),
    sa.Column('kisiarsaalan', sa.Float(), nullable=True),
    sa.Column('hisseoran', sa.Float(), nullable=True),
    sa.Column('ada', sa.Integer(), nullable=True),
    sa.Column('parsel', sa.Integer(), nullable=True),
    sa.Column('onay_durumu', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['proje_id'], ['tbl_projeler.proje_id'], ),
    sa.PrimaryKeyConstraint('veri_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_veri')
    op.drop_table('tbl_projeler')
    # ### end Alembic commands ###
