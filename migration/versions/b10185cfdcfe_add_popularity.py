"""add popularity

Revision ID: b10185cfdcfe
Revises: 
Create Date: 2016-09-23 22:06:44.584932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b10185cfdcfe'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
    	'List',
    	sa.Column('popularity', sa.Integer, nullable=False)
    )
    


def downgrade():
    pass
