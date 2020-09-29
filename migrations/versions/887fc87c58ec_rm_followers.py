"""rm followers

Revision ID: 887fc87c58ec
Revises: 8ba6b71bc1f3
Create Date: 2020-09-29 17:30:51.529293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '887fc87c58ec'
down_revision = '8ba6b71bc1f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.INTEGER(), nullable=True),
    sa.Column('followed_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###
