"""empty message

Revision ID: b5738da074cf
Revises: 9a3d26e8d74e
Create Date: 2022-08-10 23:07:10.267295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5738da074cf'
down_revision = '9a3d26e8d74e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'image_cover')
    op.add_column('user', sa.Column('cover_image', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'cover_image')
    op.add_column('recipe', sa.Column('image_cover', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
