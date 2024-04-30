"""empty message

Revision ID: 85ce76e623ab
Revises: 
Create Date: 2024-04-30 16:07:48.165379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85ce76e623ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor_patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_records_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('doctor_patient_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user_records', ['user_records_id'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('health_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_records_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('health_record_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user_records', ['user_records_id'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('age')
        batch_op.drop_column('date_of_birth')
        batch_op.drop_column('person_of_contact')
        batch_op.drop_column('address')

    with op.batch_alter_table('user_records', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('date_of_birth',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('person_of_contact',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_records', schema=None) as batch_op:
        batch_op.alter_column('person_of_contact',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('date_of_birth',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('person_of_contact', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False))

    with op.batch_alter_table('health_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('health_record_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.drop_column('user_records_id')

    with op.batch_alter_table('doctor_patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('doctor_patient_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.drop_column('user_records_id')

    # ### end Alembic commands ###
