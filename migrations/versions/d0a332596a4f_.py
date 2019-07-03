"""empty message


Revision ID: d0a332596a4f
Revises: 
Create Date: 2019-06-12 11:08:35.274000


"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0a332596a4f'

down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cloud_platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_type_id', sa.Integer(), nullable=False),
    sa.Column('platform_name', sa.String(length=255), nullable=False),
    sa.Column('ip', sa.String(length=30), nullable=False),
    sa.Column('port', sa.String(length=30), nullable=True),
    sa.Column('admin_name', sa.String(length=30), nullable=False),
    sa.Column('admin_password', sa.String(length=30), nullable=False),
    sa.Column('remarks', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('platform_name')
    )
    op.create_table('cloud_platform_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('resource_type', sa.String(length=32), nullable=False),
    sa.Column('result', sa.String(length=10), nullable=True),
    sa.Column('operation_resources_id', sa.Integer(), nullable=True),
    sa.Column('operation_event', sa.String(length=255), nullable=True),
    sa.Column('submitter', sa.String(length=32), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('event_request_id', sa.String(length=100), nullable=True),
    sa.Column('task_request_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('icon', sa.String(length=20), nullable=True),
    sa.Column('url', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('identifier', sa.String(length=50), nullable=True),
    sa.Column('is_hide', sa.Boolean(), nullable=True),
    sa.Column('is_hide_children', sa.Boolean(), nullable=True),
    sa.Column('important', sa.String(length=20), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('request_id', sa.String(length=100), nullable=False),
    sa.Column('ip', sa.String(length=20), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('status_num', sa.Integer(), nullable=True),
    sa.Column('submitter', sa.String(length=32), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('system_config',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('platform_name', sa.String(length=32), nullable=True),
    sa.Column('version_information', sa.String(length=32), nullable=True),
    sa.Column('logo', sa.String(length=128), nullable=True),
    sa.Column('copyright', sa.String(length=32), nullable=True),
    sa.Column('user_authentication_mode', sa.String(length=16), nullable=True),
    sa.Column('debug', sa.Boolean(), nullable=True),
    sa.Column('store_log', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('copyright'),
    sa.UniqueConstraint('platform_name'),
    sa.UniqueConstraint('version_information')
    )
    op.create_table('task_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.String(length=100), nullable=False),
    sa.Column('rely_task_id', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('await_execute', sa.String(length=10), nullable=False),
    sa.Column('queue_name', sa.String(length=32), nullable=False),
    sa.Column('method_name', sa.String(length=32), nullable=False),
    sa.Column('submitter', sa.String(length=32), nullable=False),
    sa.Column('enqueue_time', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('request_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('uid', sa.String(length=20), nullable=False),
    sa.Column('mobile', sa.String(length=30), nullable=False),
    sa.Column('department', sa.String(length=255), nullable=False),
    sa.Column('job', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=30), nullable=False),
    sa.Column('company', sa.String(length=100), nullable=False),
    sa.Column('sex', sa.String(length=3), nullable=False),
    sa.Column('uac', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('remarks', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=False),
    sa.Column('current_login_at', sa.DateTime(), nullable=False),
    sa.Column('last_login_ip', sa.String(length=45), nullable=False),
    sa.Column('current_login_ip', sa.String(length=45), nullable=False),
    sa.Column('login_count', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Integer(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('vm_id', sa.String(length=40), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_datastore',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('capacity', sa.String(length=32), nullable=True),
    sa.Column('used_capacity', sa.String(length=32), nullable=True),
    sa.Column('free_capacity', sa.String(length=32), nullable=True),
    sa.Column('type', sa.String(length=55), nullable=True),
    sa.Column('version', sa.String(length=55), nullable=True),
    sa.Column('uuid', sa.String(length=255), nullable=True),
    sa.Column('ssd', sa.Boolean(), nullable=False),
    sa.Column('local', sa.Boolean(), nullable=False),
    sa.Column('host', sa.String(length=55), nullable=True),
    sa.Column('ds_name', sa.String(length=255), nullable=True),
    sa.Column('ds_mor_name', sa.String(length=32), nullable=True),
    sa.Column('dc_name', sa.String(length=255), nullable=False),
    sa.Column('dc_mor_name', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_disk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vm_uuid', sa.String(length=255), nullable=False),
    sa.Column('disk_uuid', sa.String(length=255), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('label', sa.String(length=32), nullable=True),
    sa.Column('disk_size', sa.String(length=64), nullable=True),
    sa.Column('disk_type', sa.String(length=16), nullable=True),
    sa.Column('sharing', sa.String(length=16), nullable=True),
    sa.Column('disk_file', sa.String(length=255), nullable=True),
    sa.Column('shares', sa.Integer(), nullable=True),
    sa.Column('level', sa.String(length=16), nullable=True),
    sa.Column('iops', sa.String(length=16), nullable=True),
    sa.Column('cache', sa.Integer(), nullable=True),
    sa.Column('disk_mode', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('iso_name', sa.String(length=256), nullable=False),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('ds_name', sa.String(length=255), nullable=True),
    sa.Column('ds_mor_name', sa.String(length=32), nullable=True),
    sa.Column('size', sa.String(length=32), nullable=True),
    sa.Column('file_type', sa.String(length=16), nullable=True),
    sa.Column('last_change_time', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('vm_name', sa.String(length=255), nullable=False),
    sa.Column('vm_mor_name', sa.String(length=255), nullable=False),
    sa.Column('template', sa.Boolean(), nullable=False),
    sa.Column('vm_path_name', sa.String(length=255), nullable=False),
    sa.Column('memory', sa.String(length=40), nullable=False),
    sa.Column('cpu', sa.String(length=40), nullable=False),
    sa.Column('num_ethernet_cards', sa.Integer(), nullable=False),
    sa.Column('num_virtual_disks', sa.String(length=255), nullable=False),
    sa.Column('uuid', sa.String(length=255), nullable=False),
    sa.Column('instance_uuid', sa.String(length=255), nullable=False),
    sa.Column('guest_id', sa.String(length=255), nullable=False),
    sa.Column('guest_full_name', sa.String(length=255), nullable=False),
    sa.Column('host', sa.String(length=40), nullable=False),
    sa.Column('ip', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('resource_pool_name', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_network_device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('vm_uuid', sa.String(length=255), nullable=True),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('mac', sa.String(length=255), nullable=True),
    sa.Column('network_port_group', sa.String(length=255), nullable=True),
    sa.Column('address_type', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_network_distributed_switch_port_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('mor_name', sa.String(length=255), nullable=True),
    sa.Column('dc_name', sa.String(length=255), nullable=True),
    sa.Column('dc_mor_name', sa.String(length=255), nullable=True),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('switch', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_network_port_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('mor_name', sa.String(length=255), nullable=True),
    sa.Column('dc_name', sa.String(length=255), nullable=True),
    sa.Column('dc_mor_name', sa.String(length=255), nullable=True),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('host', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_resource_pool',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('dc_name', sa.String(length=255), nullable=True),
    sa.Column('dc_mor_name', sa.String(length=32), nullable=True),
    sa.Column('cluster_name', sa.String(length=255), nullable=True),
    sa.Column('cluster_mor_name', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('mor_name', sa.String(length=32), nullable=True),
    sa.Column('parent_name', sa.String(length=255), nullable=True),
    sa.Column('over_all_status', sa.String(length=32), nullable=True),
    sa.Column('cpu_expand_able_reservation', sa.String(length=32), nullable=True),
    sa.Column('cpu_reservation', sa.String(length=32), nullable=True),
    sa.Column('cpu_limit', sa.String(length=32), nullable=True),
    sa.Column('cpu_shares', sa.String(length=32), nullable=True),
    sa.Column('cpu_level', sa.String(length=32), nullable=True),
    sa.Column('cpu_over_all_usage', sa.String(length=32), nullable=True),
    sa.Column('cpu_max_usage', sa.String(length=32), nullable=True),
    sa.Column('memory_expand_able_reservation', sa.String(length=32), nullable=True),
    sa.Column('memory_reservation', sa.String(length=32), nullable=True),
    sa.Column('memory_limit', sa.String(length=32), nullable=True),
    sa.Column('memory_shares', sa.String(length=32), nullable=True),
    sa.Column('memory_level', sa.String(length=32), nullable=True),
    sa.Column('memory_over_all_usage', sa.String(length=32), nullable=True),
    sa.Column('memory_max_usage', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_snapshot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('mor_name', sa.String(length=32), nullable=True),
    sa.Column('vm_uuid', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=32), nullable=True),
    sa.Column('state', sa.String(length=32), nullable=True),
    sa.Column('snapshot_id', sa.Integer(), nullable=True),
    sa.Column('snapshot_parent_id', sa.Integer(), nullable=True),
    sa.Column('current', sa.Boolean(), nullable=False),
    sa.Column('create_time', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcenter_tree',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('dc_host_folder_mor_name', sa.String(length=255), nullable=True),
    sa.Column('dc_mor_name', sa.String(length=255), nullable=True),
    sa.Column('dc_oc_name', sa.String(length=255), nullable=True),
    sa.Column('dc_vm_folder_mor_name', sa.String(length=255), nullable=True),
    sa.Column('mor_name', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('cluster_mor_name', sa.String(length=255), nullable=True),
    sa.Column('cluster_oc_name', sa.String(length=255), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('vcenter_tree')
    op.drop_table('vcenter_snapshot')
    op.drop_table('vcenter_resource_pool')
    op.drop_table('vcenter_network_port_group')
    op.drop_table('vcenter_network_distributed_switch_port_group')
    op.drop_table('vcenter_network_device')
    op.drop_table('vcenter_instance')
    op.drop_table('vcenter_image')
    op.drop_table('vcenter_disk')
    op.drop_table('vcenter_datastore')
    op.drop_table('user_instance')
    op.drop_table('user')
    op.drop_table('task_log')
    op.drop_table('system_config')
    op.drop_table('roles_menu')
    op.drop_table('role')
    op.drop_table('request_log')
    op.drop_table('menu')
    op.drop_table('event_log')
    op.drop_table('cloud_platform_type')
    op.drop_table('cloud_platform')
    # ### end Alembic commands ###
