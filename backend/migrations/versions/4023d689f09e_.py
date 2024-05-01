"""empty message

Revision ID: 4023d689f09e
Revises: 85ce76e623ab
Create Date: 2024-05-01 07:07:09.215445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4023d689f09e'
down_revision = '85ce76e623ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('health_record_user_records_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('user_records_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_records_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('health_record_user_records_id_fkey', 'user_records', ['user_records_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
