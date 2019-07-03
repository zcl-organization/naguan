# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name
from app.main.vcenter.sync.const import PlatformType




def sync_platforms(platform_id, platforms):
    local_data = {
        item.mor_name: item.id for item in db.vcenter.vcenter_tree_list_by_platform_id(platform_id)
    }

    for platform_type, platform_data in platforms:
        sync_method[platform_type](platform_id, platform_data)
        
        mor_name = None if platform_type == PlatformType.PLATFROM else get_mor_name(platform_data)
        if mor_name in local_data.keys():
            local_data.pop(mor_name)
    
    for item in local_data.values():
        db.vcenter.vcenter_tree_delete_by_id(item)

# TODO 合并下述代码
def sync_platform_base(platform_id, platform):
    data = dict(
        tree_type=1, 
        platform_id=platform_id, 
        mor_name=None,
        name=platform
    )
    platform_base = db.vcenter.vcenter_tree_get_by_platform(platform_id, platform, 1)
    if platform_base:
        db.vcenter.vcenter_tree_update(**data)
    else:
        db.vcenter.vcenter_tree_create(**data)


def sync_platform_datacenter(platform_id, datacenter):
    platform_parent = db.vcenter.get_vcenter_tree_by_tree_type(platform_id, 1)
    data = dict(
        tree_type=2, 
        platform_id=platform_id,
        name=datacenter.name,
        dc_mor_name=get_mor_name(datacenter), 
        dc_oc_name=datacenter.name,
        mor_name=get_mor_name(datacenter),
        dc_host_folder_mor_name=get_mor_name(datacenter.hostFolder), 
        dc_vm_folder_mor_name=get_mor_name(datacenter.vmFolder),
        pid=platform_parent.id
    )
    platform_datacenter_info = db.vcenter.check_if_dc_exists_by_dc_mor_name(platform_id, get_mor_name(datacenter), 2)
    if platform_datacenter_info:
        db.vcenter.vcenter_tree_update(**data)
    else:
        db.vcenter.vcenter_tree_create(**data)


def sync_platform_cluster(platform_id, cluster):
    platform_parent = db.vcenter.get_vcenter_obj_by_mor_name(platform_id, get_mor_name(cluster.parent.parent))
    data = dict(
        tree_type=3, 
        platform_id=platform_id,
        name=cluster.name, 
        dc_mor_name=get_mor_name(cluster.parent.parent),
        dc_oc_name=cluster.parent.parent.name, 
        mor_name=get_mor_name(cluster),
        dc_host_folder_mor_name=get_mor_name(cluster.parent.parent.hostFolder),
        dc_vm_folder_mor_name=get_mor_name(cluster.parent.parent.vmFolder),
        cluster_mor_name=get_mor_name(cluster),
        cluster_oc_name=cluster.name,
        pid=platform_parent.id
    )

    platform_cluster_info = db.vcenter.vcenter_tree_get_by_cluster(platform_id, get_mor_name(cluster), 3)
    if platform_cluster_info:
        db.vcenter.vcenter_tree_update(**data)
    else:
        db.vcenter.vcenter_tree_create(**data)


def sync_platform_resourcepool(platform_id, resourcepool):
    if isinstance(resourcepool.parent, vim.ClusterComputeResource):
        parent_cluter_info = db.vcenter.vcenter_tree_get_by_cluster(platform_id, get_mor_name(resourcepool.parent), 3)
        parent_id = parent_cluter_info.id
    else:
        parent_rp_info = db.vcenter.vcenter_tree_get_by_mor_name(platform_id, get_mor_name(resourcepool.parent), 5)
        parent_id = parent_rp_info.id

    parent = resourcepool.parent
    while not isinstance(parent, vim.ClusterComputeResource):
        parent = parent.parent

    data = dict(
        tree_type=5, 
        platform_id=platform_id, 
        name=resourcepool.name,
        dc_mor_name=get_mor_name(parent.parent.parent), 
        dc_oc_name=parent.parent.parent.name,
        mor_name=get_mor_name(resourcepool),
        dc_host_folder_mor_name=get_mor_name(parent.parent.parent.hostFolder),
        dc_vm_folder_mor_name=get_mor_name(parent.parent.parent.vmFolder),
        cluster_mor_name=get_mor_name(parent),
        cluster_oc_name=parent.name, 
        pid=parent_id
    )
    platform_resourcepool_info = db.vcenter.vcenter_tree_get_by_mor_name(platform_id, get_mor_name(resourcepool), 5)
    if platform_resourcepool_info:
        db.vcenter.vcenter_tree_update(**data)
    else:
        db.vcenter.vcenter_tree_create(**data)


def sync_platform_host(platform_id, host):
    platform_parent = db.vcenter.vcenter_tree_get_by_mor_name(platform_id, get_mor_name(host.parent), 3)
    data = dict(
        tree_type=4, 
        platform_id=platform_id,
        name=host.name, 
        dc_mor_name=get_mor_name(host.parent.parent.parent),
        dc_oc_name=host.parent.parent.parent.name, 
        mor_name=get_mor_name(host),
        dc_host_folder_mor_name=get_mor_name(host.parent.parent.parent.hostFolder),
        dc_vm_folder_mor_name=get_mor_name(host.parent.parent.parent.vmFolder),
        cluster_mor_name=get_mor_name(host.parent),
        cluster_oc_name=host.parent.name,
        pid=platform_parent.id
    )

    platform_host_info = db.vcenter.vcenter_tree_get_by_mor_name(platform_id, get_mor_name(host), 4)
    if platform_host_info:
        db.vcenter.vcenter_tree_update(**data)
    else:
        db.vcenter.vcenter_tree_create(**data)


sync_method = {
    PlatformType.PLATFROM: sync_platform_base,
    PlatformType.DATACENTER: sync_platform_datacenter,
    PlatformType.CLUSTER: sync_platform_cluster,
    PlatformType.RESOURCEPOOL: sync_platform_resourcepool,
    PlatformType.HOST: sync_platform_host
}
