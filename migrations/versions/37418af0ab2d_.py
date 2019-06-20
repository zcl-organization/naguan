"""empty message

Revision ID: 37418af0ab2d
Revises: 8cfc0872a1a1
Create Date: 2019-06-20 15:26:15.103000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '37418af0ab2d'
down_revision = '8cfc0872a1a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('VCenter_clusters', sa.Column('cpu_capacity', sa.Integer(), nullable=True))
    op.add_column('VCenter_clusters', sa.Column('host_nums', sa.Integer(), nullable=True))
    op.add_column('VCenter_clusters', sa.Column('used_capacity', sa.BigInteger(), nullable=True))
    op.add_column('VCenter_clusters', sa.Column('vm_nums', sa.Integer(), nullable=True))
    op.drop_column('VCenter_clusters', 'free_capacity')
    op.drop_column('VCenter_clusters', 'cpu_cores')
    op.drop_column('VCenter_clusters', 'cpu_mhz')
    op.add_column('vcenter_datacenter', sa.Column('cpu_capacity', sa.Integer(), nullable=True))
    op.add_column('vcenter_datacenter', sa.Column('used_capacity', sa.BigInteger(), nullable=True))
    op.drop_column('vcenter_datacenter', 'free_capacity')
    op.drop_column('vcenter_datacenter', 'cpu_cores')
    op.drop_column('vcenter_datacenter', 'cpu_mhz')
    op.add_column('vcenter_host', sa.Column('used_capacity', sa.BigInteger(), nullable=True))
    op.drop_column('vcenter_host', 'free_capacity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vcenter_host', sa.Column('free_capacity', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True))
    op.drop_column('vcenter_host', 'used_capacity')
    op.add_column('vcenter_datacenter', sa.Column('cpu_mhz', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('vcenter_datacenter', sa.Column('cpu_cores', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('vcenter_datacenter', sa.Column('free_capacity', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True))
    op.drop_column('vcenter_datacenter', 'used_capacity')
    op.drop_column('vcenter_datacenter', 'cpu_capacity')
    op.add_column('VCenter_clusters', sa.Column('cpu_mhz', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('VCenter_clusters', sa.Column('cpu_cores', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('VCenter_clusters', sa.Column('free_capacity', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True))
    op.drop_column('VCenter_clusters', 'vm_nums')
    op.drop_column('VCenter_clusters', 'used_capacity')
    op.drop_column('VCenter_clusters', 'host_nums')
    op.drop_column('VCenter_clusters', 'cpu_capacity')
    # ### end Alembic commands ###
