"""add enum reassign_model

Revision ID: fdb5d50f8331
Revises: 4cb1bd466ce1
Create Date: 2020-08-12 00:14:46.101377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdb5d50f8331'
down_revision = '4cb1bd466ce1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("COMMIT")
    op.execute("ALTER TYPE log ADD VALUE 'reassign_model'")
    op.execute("ALTER TYPE repetition ADD VALUE 'karl50'")
    op.execute("ALTER TYPE repetition ADD VALUE 'karl85'")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
