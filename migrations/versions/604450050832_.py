"""empty message

Revision ID: 604450050832
Revises: 4126eab60d78
Create Date: 2019-06-18 18:34:13.350000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '604450050832'
down_revision = '4126eab60d78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('licenses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('licenseKey', sa.String(length=128), nullable=True),
    sa.Column('editionKey', sa.String(length=128), nullable=True),
    sa.Column('used', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_host',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('mor_name', sa.String(length=32), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('power_state', sa.String(length=32), nullable=True),
    sa.Column('maintenance_mode', sa.Boolean(), nullable=True),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('uuid', sa.String(length=128), nullable=True),
    sa.Column('cpu', sa.String(length=128), nullable=True),
    sa.Column('ram', sa.String(length=128), nullable=True),
    sa.Column('used_ram', sa.String(length=128), nullable=True),
    sa.Column('rom', sa.String(length=128), nullable=True),
    sa.Column('used_rom', sa.String(length=128), nullable=True),
    sa.Column('cpu_model', sa.String(length=32), nullable=True),
    sa.Column('version', sa.String(length=32), nullable=True),
    sa.Column('image', sa.String(length=32), nullable=True),
    sa.Column('build', sa.String(length=32), nullable=True),
    sa.Column('full_name', sa.String(length=64), nullable=True),
    sa.Column('boot_time', sa.String(length=32), nullable=True),
    sa.Column('uptime', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_vswitch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('mor_name', sa.String(length=32), nullable=True),
    sa.Column('host_name', sa.String(length=255), nullable=True),
    sa.Column('host_mor_name', sa.String(length=32), nullable=True),
    sa.Column('mtu', sa.Integer(), nullable=True),
    sa.Column('num_of_port', sa.Integer(), nullable=True),
    sa.Column('nics', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'event_log', 'result',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=10),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column(u'menu', 'is_hide',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column(u'menu', 'is_hide_children',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column(u'system_config', 'debug',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column(u'user', 'active',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column(u'user', 'is_superuser',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column(u'vcenter_datastore', 'local',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column(u'vcenter_datastore', 'ssd',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column(u'vcenter_instance', 'template',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column(u'vcenter_snapshot', 'current',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'vcenter_snapshot', 'current',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column(u'vcenter_instance', 'template',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column(u'vcenter_datastore', 'ssd',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column(u'vcenter_datastore', 'local',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column(u'user', 'is_superuser',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column(u'user', 'active',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column(u'system_config', 'debug',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column(u'menu', 'is_hide_children',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column(u'menu', 'is_hide',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column(u'event_log', 'result',
               existing_type=sa.Boolean(),
               type_=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=10),
               existing_nullable=True)
    op.drop_table('vcenter_vswitch')
    op.drop_table('vcenter_host')
    op.drop_table('licenses')
    # ### end Alembic commands ###
