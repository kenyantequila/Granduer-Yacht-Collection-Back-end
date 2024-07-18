"""Add num_tickets column to booking table

Revision ID: fff97f0de61a
Revises: 1e472e324a12
Create Date: 2024-07-18 20:21:41.686853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fff97f0de61a'
down_revision = '1e472e324a12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num_tickets', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('num_days', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('total_price', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('booking_date', sa.DateTime(), nullable=True))
        batch_op.drop_column('start_date')
        batch_op.drop_column('end_date')
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('end_date', sa.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('start_date', sa.DATETIME(), nullable=False))
        batch_op.drop_column('booking_date')
        batch_op.drop_column('total_price')
        batch_op.drop_column('num_days')
        batch_op.drop_column('num_tickets')

    # ### end Alembic commands ###