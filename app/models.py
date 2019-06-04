# -*- coding:utf-8 -*-
from exts import db
from flask_security import Security, UserMixin, RoleMixin, login_required
from passlib.apps import custom_app_context as pwd_context
from config import config, UPLOAD_DIR, BASE_DIR
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from flask import current_app
from config import config
import os
import datetime


# roles_users = db.Table('roles_users',
#                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))


class Roles(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    roleUsers = db.relationship('RolesUsers', backref="role", lazy="dynamic")

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


# User class
class Users(db.Model, UserMixin):
    # Our User has six fields: ID, email, password, active, confirmed_at and roles. The roles field represents a
    # many-to-many relationship using the roles_users table. Each user may have no role, one role, or multiple roles.
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 用户id
    username = db.Column(db.String(100), nullable=False, unique=True)  # 用户名
    password = db.Column(db.String(128), nullable=False)  # 密码
    first_name = db.Column(db.String(100), nullable=False)  # first name
    email = db.Column(db.String(120), nullable=False, unique=True)  # 邮箱
    uid = db.Column(db.String(20), nullable=False, default='')  # uid
    mobile = db.Column(db.String(30), nullable=False)  # 手机
    department = db.Column(db.String(255), nullable=False)  # 部门
    job = db.Column(db.String(100), nullable=False)  # 工作
    location = db.Column(db.String(30), nullable=False)  # 地点
    company = db.Column(db.String(100), nullable=False)  # 公司
    sex = db.Column(db.String(3), nullable=False)  # 性别
    uac = db.Column(db.Integer)  # UAC
    active = db.Column(db.Boolean, nullable=False)  # 激活状态
    is_superuser = db.Column(db.Boolean, nullable=False)  # 是否是超管
    remarks = db.Column(db.String(255))  # 备注
    date_created = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.now())  # 创建时间
    confirmed_at = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.now())  # 确认时间

    last_login_at = db.Column(db.DateTime, nullable=False,
                              default=lambda: datetime.datetime.now())  # 上次登录时间
    current_login_at = db.Column(db.DateTime, nullable=False,
                                 default=lambda: datetime.datetime.now())  # 当前登录时间
    last_login_ip = db.Column(db.String(45), nullable=False)  # 上传登录IP
    current_login_ip = db.Column(db.String(45), nullable=False)  # 当前登录IP
    login_count = db.Column(db.Integer, nullable=False)  # 登录次数
    is_deleted = db.Column(db.Integer, default=0)
    deleted_at = db.Column(db.DateTime)  # 删除时间

    roles = db.relationship(
        'Roles',
        secondary='roles_users',
        lazy="dynamic",
        backref=db.backref('users', lazy='dynamic')
    )

    rolesUser = db.relationship('RolesUsers', backref="user", lazy="dynamic")

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'id': self.id, 'username': self.username})

    @staticmethod
    def get_hash_password(password):
        return pwd_context.encrypt(password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            code = 1
        except SignatureExpired:
            data = ''
            code = 2
        except BadSignature:
            data = ''
            code = 3
        # user = User.query.get(data['id'])
        return data, code


# 系统配置
class SystemConfig(db.Model):
    __table_name__ = 'system_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #  平台名称
    platform_name = db.Column(db.String(32), unique=True)
    # 版本信息
    version_information = db.Column(db.String(32), unique=True)

    logo = db.Column(db.String(128), default=UPLOAD_DIR + 'logo.png')
    # 版权
    copyright = db.Column(db.String(32), unique=True)
    # 用户验证模式
    user_authentication_mode = db.Column(db.String(16))
    # 是否开启调试模式
    debug = db.Column(db.Boolean, default=False)
    # 日志存储
    store_log = db.Column(db.String(100), default=BASE_DIR + 'app\\static\\store.log')
    ##


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 菜单项id
    icon = db.Column(db.String(20), default='')  # 图标
    url = db.Column(db.String(128), nullable=False)  # url
    name = db.Column(db.String(128), nullable=False)  # 名称
    identifier = db.Column(db.String(50), default='')  # 标识
    is_hide = db.Column(db.Boolean, default=False)  # 时候隐藏
    is_hide_children = db.Column(db.Boolean, default=False)  # 是否隐藏子菜单
    important = db.Column(db.String(20), default=None)  # 重要
    parent_id = db.Column(db.Integer, default=0)  # 父菜单id
    date_created = db.Column(db.DateTime, nullable=True,
                             default=lambda: datetime.datetime.now())  # 创建时间


class RequestLog(db.Model):
    __tablename__ = 'request_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.String(100), nullable=False)  # 请求ID
    ip = db.Column(db.String(20), nullable=False)  # 请求ip
    url = db.Column(db.String(255), nullable=False)  # url（请求方法+api）
    status_num = db.Column(db.Integer)  # 状态值
    submitter = db.Column(db.String(32), nullable=False)  # 提交者
    time = db.Column(db.DateTime, default=datetime.datetime.now())  # 创建时间
    # event_logs = db.relationship('EventLog', backref='request_logs', lazy=True)  # 关联表


class TaskLog(db.Model):
    __tablenname__ = 'task_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(100), nullable=False)  # 任务ID
    rely_task_id = db.Column(db.String(100))  # 依赖任务
    status = db.Column(db.String(10), nullable=False)  # 状态
    await_execute = db.Column(db.String(10), nullable=False)  # 等待/执行
    queue_name = db.Column(db.String(32), nullable=False)  # 队列名
    method_name = db.Column(db.String(32), nullable=False)  # 方法名
    submitter = db.Column(db.String(32), nullable=False)  # 提交者
    enqueue_time = db.Column(db.DateTime, default=datetime.datetime.now())  # 入队时间
    start_time = db.Column(db.DateTime)  # 开始时间
    end_time = db.Column(db.DateTime)  # 结束时间
    request_id = db.Column(db.String(100))  # 请求ID
    # event_logs = db.relationship('EventLog', backref='task_logs', lazy=True)  # 关联表


class EventLog(db.Model):
    __tablename__ = 'event_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_type = db.Column(db.String(32), nullable=False)  # 操作资源类型
    result = db.Column(db.String(10))  # 操作结果
    operation_resources_id = db.Column(db.Integer)  # 操作资源ID
    operation_event = db.Column(db.String(255))  # 操作事件
    submitter = db.Column(db.String(32), nullable=False)  # 提交者
    time = db.Column(db.DateTime, default=datetime.datetime.now())  # 创建时间
    # 外键
    # event_request_id = db.Column(db.String, db.ForeignKey(RequestLog.request_id))  # 请求ID
    # task_request_id = db.Column(db.String, db.ForeignKey(TaskLog.task_id))  # 任务ID

    event_request_id = db.Column(db.String(100))  # 请求ID
    task_request_id = db.Column(db.String(100))  # 任务ID


class VCenterVm(db.Model):
    __tablename__ = 'vcenter_instance'

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, nullable=False)  # 所属于平台
    vm_name = db.Column(db.String(255), nullable=False)  # 云主机名称
    vm_mor_name = db.Column(db.String(255), nullable=False)
    template = db.Column(db.Boolean, nullable=False)
    vm_path_name = db.Column(db.String(255), nullable=False)
    memory = db.Column(db.String(40), nullable=False)  # 内存
    # memory_used = db.Column(db.String(40), nullable=False)                      # 已使用内存
    cpu = db.Column(db.String(40), nullable=False)  # 总cpu
    # cpu_used = db.Column(db.String(40), nullable=False)                         # 已使用cpu
    num_ethernet_cards = db.Column(db.Integer, nullable=False)
    num_virtual_disks = db.Column(db.String(255), nullable=False)
    uuid = db.Column(db.String(255), nullable=False)
    instance_uuid = db.Column(db.String(255), nullable=False)
    guest_id = db.Column(db.String(255), nullable=False)  # 镜像id
    guest_full_name = db.Column(db.String(255), nullable=False)
    host = db.Column(db.String(40), nullable=False)  # 所属HOST
    ip = db.Column(db.String(20))  # ip
    status = db.Column(db.String(40))
    resource_pool_name = db.Column(db.String(32))
    created_at = db.Column(db.DateTime)  # 创建时间


class UsersInstances(db.Model):
    __tablename__ = 'user_instance'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    vm_id = db.Column(db.String(40), nullable=False)
    platform_id = db.Column(db.Integer, nullable=False)

    # user = db.relationship('User', uselist=False, backref=db.backref('intids', lazy='dynamic'))
    # intid = db.relationship('Instance', uselist=False, backref=db.backref('intids', lazy='dynamic'))

    def __repr__(self):
        return '<UserID:%r / IntID:%r>' % (self.user_id, self.int_id)

    def __unicode__(self):
        return self.id


class CloudPlatformType(db.Model):
    __tablename__ = 'cloud_platform_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


class CloudPlatform(db.Model):
    __tablename__ = 'cloud_platform'
    id = db.Column(db.Integer, primary_key=True)
    platform_type_id = db.Column(db.Integer, nullable=False)
    platform_name = db.Column(db.String(255), nullable=False, unique=True)
    ip = db.Column(db.String(30), nullable=False)
    port = db.Column(db.String(30))
    admin_name = db.Column(db.String(30), nullable=False)
    admin_password = db.Column(db.String(30), nullable=False)
    remarks = db.Column(db.String(255))  # 备注


class VCenterTree(db.Model):
    __tablename__ = 'vcenter_tree'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)  # 类型

    platform_id = db.Column(db.Integer, nullable=False, )  # platform_id
    dc_host_folder_mor_name = db.Column(db.String(255))
    dc_mor_name = db.Column(db.String(255))
    dc_oc_name = db.Column(db.String(255))
    dc_vm_folder_mor_name = db.Column(db.String(255))
    mor_name = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False)
    cluster_mor_name = db.Column(db.String(255))
    cluster_oc_name = db.Column(db.String(255))
    pid = db.Column(db.Integer)


class VCenterNetworkPortGroup(db.Model):
    __tablename__ = 'vcenter_network_port_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    mor_name = db.Column(db.String(255))
    dc_name = db.Column(db.String(255))
    dc_mor_name = db.Column(db.String(255))
    platform_id = db.Column(db.Integer)


class VCenterNetworkDevice(db.Model):
    __tablename__ = 'vcenter_network_device'
    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer)
    vm_uuid = db.Column(db.String(255))
    label = db.Column(db.String(255))
    mac = db.Column(db.String(255))
    network_port_group = db.Column(db.String(255))
    address_type = db.Column(db.String(255))


class VCenterDataStore(db.Model):
    __tablename__ = 'vcenter_datastore'
    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer)
    # name = db.Column(db.String(255))
    capacity = db.Column(db.String(32))
    used_capacity = db.Column(db.String(32))
    free_capacity = db.Column(db.String(32))
    type = db.Column(db.String(55))
    version = db.Column(db.String(55))
    uuid = db.Column(db.String(255))
    ssd = db.Column(db.Boolean, nullable=False)
    local = db.Column(db.Boolean, nullable=False)
    host = db.Column(db.String(55))
    ds_name = db.Column(db.String(255))
    ds_mor_name = db.Column(db.String(32))
    dc_name = db.Column(db.String(255), nullable=False)
    dc_mor_name = db.Column(db.String(32))


class VCenterDisk(db.Model):
    __tablename__ = 'vcenter_disk'
    id = db.Column(db.Integer, primary_key=True)
    vm_uuid = db.Column(db.String(255), nullable=False)
    disk_uuid = db.Column(db.String(255), nullable=False)
    platform_id = db.Column(db.Integer)
    label = db.Column(db.String(32))
    disk_size = db.Column(db.String(64))  #
    disk_type = db.Column(db.String(16))  # 类型
    sharing = db.Column(db.String(16))  # 共享
    disk_file = db.Column(db.String(255))
    shares = db.Column(db.Integer)  # 份额数
    level = db.Column(db.String(16))  # 份额 等级
    iops = db.Column(db.String(16))
    cache = db.Column(db.Integer)
    disk_mode = db.Column(db.String(16))


class VCenterImage(db.Model):
    __tablename__ = 'vcenter_image'
    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer)
    iso_name = db.Column(db.String(256), nullable=False)  # name
    path = db.Column(db.String(256))  # 路径
    ds_name = db.Column(db.String(255))  #
    ds_mor_name = db.Column(db.String(32))
    size = db.Column(db.String(32))
    file_type = db.Column(db.String(16), default='ISO')  # 文件类型
    last_change_time = db.Column(db.String(32))  # 修改时间


class VCenterSnapshot(db.Model):
    __tablename__ = 'vcenter_snapshot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    mor_name = db.Column(db.String(32))
    vm_uuid = db.Column(db.String(255))
    description = db.Column(db.String(32))
    state = db.Column(db.String(32))
    snapshot_id = db.Column(db.Integer)
    snapshot_parent_id = db.Column(db.Integer)
    current = db.Column(db.Boolean, nullable=False)
    create_time = db.Column(db.String(32))


class VCenterResourcePool(db.Model):
    __tablename__ = 'vcenter_resource_pool'
    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer)
    dc_name = db.Column(db.String(255))
    dc_mor_name = db.Column(db.String(32))
    cluster_name = db.Column(db.String(255))
    cluster_mor_name = db.Column(db.String(32))
    name = db.Column(db.String(255))
    mor_name = db.Column(db.String(32))
    parent_name = db.Column(db.String(255))

    over_all_status = db.Column(db.String(32))
    cpu_expand_able_reservation = db.Column(db.String(32))
    cpu_reservation = db.Column(db.String(32))
    cpu_limit = db.Column(db.String(32))
    cpu_shares = db.Column(db.String(32))
    cpu_level = db.Column(db.String(32))
    cpu_over_all_usage = db.Column(db.String(32))
    cpu_max_usage = db.Column(db.String(32))
    memory_expand_able_reservation = db.Column(db.String(32))
    memory_reservation = db.Column(db.String(32))
    memory_limit = db.Column(db.String(32))
    memory_shares = db.Column(db.String(32))
    memory_level = db.Column(db.String(32))
    memory_over_all_usage = db.Column(db.String(32))
    memory_max_usage = db.Column(db.String(32))


class RolesMenus(db.Model):
    __tablename__ = 'roles_menu'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer)
