# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_resourcepools(platform_id, resource_pools):
    """
    同步一组资源池数据
    """
    local_data = {
        item.mor_name: item.id for item in db.resource_pool.get_resource_pool_list(platform_id=platform_id)
    }

    for resource_pool in resource_pools:
        parent = resource_pool.parent
        sync_resourcepool(platform_id, resource_pool, parent)
        resource_pool_mor_name = get_mor_name(resource_pool)
        if resource_pool_mor_name in local_data.keys():
            local_data.pop(resource_pool_mor_name)
        
    for item in local_data.values():
        db.resource_pool.delete_resource_pool(item)


def sync_resourcepool(platform_id, resource_pool, parent):
    """
    同步单个资源池数据
    """
    if isinstance(resource_pool.parent, vim.ResourcePool):
        # 找到归属的集群数据
        while not isinstance(parent, vim.ClusterComputeResource):
            parent = parent.parent
            
        parent_local = db.resource_pool.get_resource_pool_by_datas(
            platform_id=platform_id, 
            dc_name=parent.parent.parent.name,  # cluster.folder.datacenter
            cluster_name=parent.name, 
            name=resource_pool.parent.name, 
            mor_name=get_mor_name(resource_pool.parent)
        )
        parent_id = parent_local.id
    else:
        parent_id = -1

    data = dict(
        platform_id=platform_id, 
        dc_name=parent.parent.parent.name,  # cluster.folder.datacenter
        dc_mor_name=get_mor_name(parent.parent.parent),  # cluster.folder.datacenter
        cluster_name=parent.name,
        cluster_mor_name=get_mor_name(parent), 
        name=resource_pool.name, 
        mor_name=get_mor_name(resource_pool),
        parent_name=resource_pool.parent.name, 
        parent_id=parent_id, 
        over_all_status=resource_pool.overallStatus,
        cpu_expand_able_reservation=resource_pool.summary.config.cpuAllocation.expandableReservation,
        cpu_reservation=resource_pool.summary.config.cpuAllocation.reservation,
        cpu_limit=resource_pool.summary.config.cpuAllocation.limit,
        cpu_shares=resource_pool.summary.config.cpuAllocation.shares.shares,
        cpu_level=resource_pool.summary.config.cpuAllocation.shares.shares,
        cpu_over_all_usage=resource_pool.summary.runtime.cpu.overallUsage,
        cpu_max_usage=resource_pool.summary.runtime.cpu.maxUsage,
        memory_expand_able_reservation=resource_pool.summary.config.memoryAllocation.expandableReservation,
        memory_reservation=resource_pool.summary.config.memoryAllocation.reservation,
        memory_limit=resource_pool.summary.config.memoryAllocation.limit,
        memory_shares=resource_pool.summary.config.memoryAllocation.shares.shares,
        memory_level=resource_pool.summary.config.memoryAllocation.shares.level,
        memory_over_all_usage=resource_pool.summary.runtime.memory.overallUsage,
        memory_max_usage=resource_pool.summary.runtime.memory.maxUsage
    )

    resource_pool_info = db.resource_pool.get_rp_by_mor_name(platform_id, get_mor_name(resource_pool))
    if resource_pool_info:
        data['rp_id'] = resource_pool_info.id
        db.resource_pool.update_resource_pool(**data)
    else:
        db.resource_pool.create_resource_pool(**data)
