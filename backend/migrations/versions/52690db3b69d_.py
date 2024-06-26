"""empty message

Revision ID: 52690db3b69d
Revises: cc2e428dfe94
Create Date: 2024-05-01 14:11:00.763601

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = '52690db3b69d'
down_revision = 'cc2e428dfe94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('conversation_vector', schema=None) as batch_op:
        batch_op.alter_column('vector',
               existing_type=pgvector.sqlalchemy.Vector(dim=1538),
               type_=pgvector.sqlalchemy.Vector(dim=300),
               existing_nullable=True)

    with op.batch_alter_table('doctor_patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_records_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('doctor_patient_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user_records', ['user_records_id'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('health_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doctor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'doctor', ['doctor_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_record', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('doctor_id')

    with op.batch_alter_table('doctor_patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('doctor_patient_user_id_fkey', 'user_records', ['user_id'], ['id'])
        batch_op.drop_column('user_records_id')

    with op.batch_alter_table('conversation_vector', schema=None) as batch_op:
        batch_op.alter_column('vector',
               existing_type=pgvector.sqlalchemy.Vector(dim=300),
               type_=pgvector.sqlalchemy.Vector(dim=1538),
               existing_nullable=True)

    # ### end Alembic commands ###
