# -*- coding:utf-8 -*-
from flask_restful import Api
from flasgger import Swagger
from app.main.base.apis.system import System
from app.main.base.apis.system_logo import SystemLogo

from app.main.base.apis.users import UserManage
from app.main.base.apis.auth import AuthManage
from app.main.base.apis.menus import MenuManage
from app.main.base.apis.login import LoginManage
from app.main.base.apis.cloud_platform import CloudPlatformManage
from app.main.base.apis.platform_type import PlatformTypeMg

from app.main.base.apis.event_logs import LogEvent
from app.main.base.apis.request_logs import LogRequest
from app.main.base.apis.task_logs import LogTask

from app.main.base.apis.role import RoleManage
from app.main.base.apis.roles_users import RolesUsersManage
from app.main.vcenter.apis.clusters import ClustersManage
from app.main.vcenter.apis.datacenters import DataCenterManage

from app.main.vcenter.apis.instances import InstanceManage
from app.main.vcenter.apis.vcenter import VCenterManage
from app.main.vcenter.apis.images import ImageManage
from app.main.vcenter.apis.network_port_group import NetworkPortGroupManage
from app.main.vcenter.apis.datastores import DataStoreManage
from app.main.vcenter.apis.disks import DiskManage
from app.main.vcenter.apis.network_devices import NetWorkManage
from app.main.vcenter.apis.snapshots import SnapshotManage
from app.main.vcenter.apis.resource_pool import ResourcePoolManage
from app.main.vcenter.apis.ovf import OvfManage


api = Api()


def restful_init(app):
    api.init_app(app)


def swagger_init(app):
    template = {
        "swagger": "2.0",
        "info": {
            "title": "KStack NaGuan API",
            "description": "KStack NaGuan API",
            "contact": {
                "responsibleOrganization": "KStack NaGuan API",
                "responsibleDeveloper": "KStack NaGuan API",
                "email": "kpy@gmail.com",
                "url": "#",
            },
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "basicAuth": {
                "type": "basic"
            },
            # "apiKey": {
            #     "type": "apiKey",
            #     "in": "header",
            #     "name": "x-access-token"
            # }
        },
        "tags": [{
            "name": "Auth",
            "description": "Operations about authorization service."
        }
        ],
    }

    Swagger(app, template=template)


# 登录管理
api.add_resource(LoginManage, '/api/v1.0/login', methods=['POST'], endpoint='LoginMg')

# 用户管理
api.add_resource(UserManage, '/api/v1.0/user', methods=['POST', 'GET'], endpoint='UserMg')
api.add_resource(UserManage, '/api/v1.0/user/<id>', methods=['DELETE', 'PUT'], endpoint='UserMgById')
api.add_resource(AuthManage, '/api/v1.0/sso/auth', endpoint='AuthMg')

# 菜单管理
api.add_resource(MenuManage, '/api/v1.0/menu', methods=['GET', 'POST'], endpoint='MenuMg')
api.add_resource(MenuManage, '/api/v1.0/menu/<id>', methods=['PUT', 'DELETE'], endpoint='MenuMgById')

# 系统配置
api.add_resource(System, '/api/v1.0/system/config')
api.add_resource(SystemLogo, '/api/v1.0/system/logo/')

# 请求日志
api.add_resource(LogRequest, '/api/v1.0/log/request', methods=['GET'], endpoint='LogRequest')
api.add_resource(LogRequest, '/api/v1.0/log/request/<int:id>', methods=['DELETE'], endpoint='LogRequestById')

# 事件日志
api.add_resource(LogEvent, '/api/v1.0/log/event', methods=['GET'], endpoint='LogEvent')
api.add_resource(LogEvent, '/api/v1.0/log/event/<int:id>', methods=['DELETE'], endpoint='LogEventById')

# 任务日志
api.add_resource(LogTask, '/api/v1.0/log/task', methods=['GET'], endpoint='LogTask')
api.add_resource(LogTask, '/api/v1.0/log/task/<int:id>', methods=['DELETE'], endpoint='LogTaskById')

# 第三方平台管理
api.add_resource(CloudPlatformManage, '/api/v1.0/platform', methods=['GET', 'POST'], endpoint='PlatformMg')
api.add_resource(CloudPlatformManage, '/api/v1.0/platform/<id>', methods=['PUT', 'DELETE'], endpoint='PlatformMgById')

# 第三方平台类型管理
api.add_resource(PlatformTypeMg, '/api/v1.0/platform_type', methods=['GET', 'POST'], endpoint='PfTypeMg')
api.add_resource(PlatformTypeMg, '/api/v1.0/platform_type/<id>', methods=['PUT', 'DELETE'], endpoint='PfTypeMgById')

# 角色管理
api.add_resource(RoleManage, '/api/v1.0/role', methods=['GET', 'POST'], endpoint='RoleManage')
api.add_resource(RoleManage, '/api/v1.0/role/<int:id>', methods=['DELETE', 'PUT'], endpoint='RoleManageById')

# 用户角色管理
api.add_resource(RolesUsersManage, '/api/v1.0/role_user', methods=['GET', 'POST', 'PUT', 'DELETE'],
                 endpoint='RoleUserMg')

# vCenter 信息同步
api.add_resource(VCenterManage, '/api/v1.0/vCenter/tree', methods=['GET', 'POST'], endpoint='TreeMg')
api.add_resource(InstanceManage, '/api/v1.0/vCenter/vm', methods=['GET', 'POST', 'PUT'], endpoint='VmMg')
api.add_resource(InstanceManage, '/api/v1.0/vCenter/vm/<int:id>/<string:uuid>', methods=['DELETE'], endpoint='VmMgDel')
api.add_resource(ImageManage, '/api/v1.0/vCenter/image', methods=['GET', 'POST', 'PUT', 'DELETE'], endpoint='ImageMg')

# vCenter 网络端口组管理
api.add_resource(NetworkPortGroupManage, '/api/v1.0/vCenter/network_port_group/',
                 methods=['GET'], endpoint='NetworkPortGroupMg')

# vCenter datastore
api.add_resource(DataStoreManage, '/api/v1.0/vCenter/DataStore', methods=['GET'],
                 endpoint='DataStoreMg')
# vCenter DataCenter
api.add_resource(DataCenterManage, '/api/v1.0/vCenter/datacenter', methods=['POST'],
                 endpoint='DataCenterMg')
api.add_resource(DataCenterManage, '/api/v1.0/vCenter/datacenter/<int:id>', methods=['DELETE'],
                 endpoint='DataCenterMgDel')
api.add_resource(ClustersManage, '/api/v1.0/vCenter/clusters', methods=['POST'],
                 endpoint='ClustersManage')
api.add_resource(ClustersManage, '/api/v1.0/vCenter/clusters/<int:id>', methods=['DELETE'],
                 endpoint='ClustersManageDel')

# vCenter disk
api.add_resource(DiskManage, '/api/v1.0/vCenter/disk', methods=['GET', 'POST', 'DELETE'], endpoint='DiskMg')

# vCenter network device
api.add_resource(NetWorkManage, '/api/v1.0/vCenter/network', methods=['GET', 'POST', 'DELETE'],
                 endpoint='NetworkDeviceMg')

# vCenter snapshot
api.add_resource(SnapshotManage, '/api/v1.0/vCenter/snapshot', methods=['GET', 'POST'],
                 endpoint='SnapshotMg')
api.add_resource(SnapshotManage, '/api/v1.0/vCenter/snapshot/<int:snapshot_id>', methods=['DELETE'],
                 endpoint='SnapshotMgDel')

# vCenter resource_pool
api.add_resource(ResourcePoolManage, '/api/v1.0/vCenter/resource_pool', methods=['GET'],
                 endpoint='ResourcePoolMg')

api.add_resource(OvfManage, '/api/v1.0/vCenter/ovf', methods=['GET'],
                 endpoint='OvfManage')
