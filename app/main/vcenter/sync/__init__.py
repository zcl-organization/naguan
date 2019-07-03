# -*- coding: utf-8 -*-
from pyVmomi import vim

from app.main.vcenter.sync.const import SyncOperation
from app.main.vcenter.sync.flat import sync_info

from app.main.vcenter.sync.platform.datacenter.datacenter import sync_datacenters
from app.main.vcenter.sync.platform.datacenter.network_portgroup import sync_network_portgroup
from app.main.vcenter.sync.platform.datacenter.dvswitch import sync_dvswitchs
from app.main.vcenter.sync.platform.datacenter.datastore import sync_datastores
from app.main.vcenter.sync.platform.datacenter.cluster.cluster import sync_clusters
from app.main.vcenter.sync.platform.datacenter.cluster.resource_pool import sync_resourcepools
from app.main.vcenter.sync.platform.datacenter.cluster.host.host import sync_hosts
from app.main.vcenter.sync.platform.datacenter.cluster.host.vswitch import sync_vswitchs
from app.main.vcenter.sync.platform.datacenter.cluster.host.vm import sync_vm_instances
from app.main.vcenter.sync.platform.platform import sync_platforms


deal_map = {
    SyncOperation.PLATFORM: sync_platforms,
    SyncOperation.DATACENTER: sync_datacenters,
    SyncOperation.PORTGROUP: sync_network_portgroup,
    SyncOperation.DVSWITCH: sync_dvswitchs,
    SyncOperation.DATASTORE: sync_datastores,
    SyncOperation.CLUSTER: sync_clusters,
    SyncOperation.RESOURCEPOOL: sync_resourcepools,
    SyncOperation.HOST: sync_hosts,
    SyncOperation.VSWITCH: sync_vswitchs,
    SyncOperation.VM: sync_vm_instances
}


def consumption_sync(info):
    """
    处理同步
    TODO 收集处理删除  无意义的id
    """
    for operation, value in info.items():
        for platform, datas in value.items():
            print operation, "Start", platform
            deal_map[operation](platform, datas)
            print operation, "Over", platform


def sync_all_new(platform_id):
    consumption_sync(sync_info(1))


# if __name__ == "__main__":
#     from mock import Mock
#     from manage import app
#     platforms = [
#         {
#             'ip': '192.168.78.205', 
#             'name': 'administrator@vsphere.local', 
#             'password': 'Aiya@2018', 
#             'port': '443'
#         },
#     ]
#     from app.main.vcenter.utils.base import VCenter
#     from app.main.base.control import cloud_platform
#     cloud_platform.platform_list = Mock(return_value=platforms)

#     with app.test_request_context():
#         data = sync_info(1)
#         consumption_sync(data)
#         print len(data)
