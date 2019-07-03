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


# 处理函数映射
METHODSMAP = {
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


def consumption_sync(platform_id, info):
    """
    处理同步 
    TODO print -> log
    """
    for operation, value in info.items():
        print operation, "Start", platform_id
        METHODSMAP[operation](platform_id, value)
        print operation, "Over", platform_id


def sync_all_new(platform_id):
    consumption_sync(platform_id, sync_info(platform_id))
