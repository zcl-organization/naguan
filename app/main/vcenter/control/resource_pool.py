# -*- coding:utf-8 -*-
import time

from pyVmomi import vmodl
from pyVmomi import vim
from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name
from app.exts import celery


@celery.task()
def sync_resourcepool(platform, dc, cluster, si, content):
    print ('sync_rp_start:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))
    obj = content.viewManager.CreateContainerView(dc, [vim.ResourcePool], True)
    resourcepools = obj.view

    for rp in resourcepools:

        rp_db = db.resource_pool.get_rp_by_mor_name(get_mor_name(rp))

        if rp_db:
            # print('update 1')
            update_resource_pool(rp_id=rp_db.id, platform_id=platform['id'], dc_name=dc.name,
                                 dc_mor_name=get_mor_name(dc), cluster_name=cluster.name,
                                 cluster_mor_name=get_mor_name(cluster), name=rp.name, mor_name=get_mor_name(rp),
                                 parent_name=rp.parent.name, over_all_status=rp.overallStatus,
                                 cpu_expand_able_reservation=rp.summary.config.cpuAllocation.expandableReservation,
                                 cpu_reservation=rp.summary.config.cpuAllocation.reservation,
                                 cpu_limit=rp.summary.config.cpuAllocation.limit,
                                 cpu_shares=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_level=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_over_all_usage=rp.summary.runtime.cpu.overallUsage,
                                 cpu_max_usage=rp.summary.runtime.cpu.maxUsage,
                                 memory_expand_able_reservation=rp.summary.config.memoryAllocation.expandableReservation,
                                 memory_reservation=rp.summary.config.memoryAllocation.reservation,
                                 memory_limit=rp.summary.config.memoryAllocation.limit,
                                 memory_shares=rp.summary.config.memoryAllocation.shares.shares,
                                 memory_level=rp.summary.config.memoryAllocation.shares.level,
                                 memory_over_all_usage=rp.summary.runtime.memory.overallUsage,
                                 memory_max_usage=rp.summary.runtime.memory.maxUsage)
            # print('update 2')
        else:
            # print('create 1')
            create_resource_pool(platform_id=platform['id'], dc_name=dc.name,
                                 dc_mor_name=get_mor_name(dc), cluster_name=cluster.name,
                                 cluster_mor_name=get_mor_name(cluster), name=rp.name, mor_name=get_mor_name(rp),
                                 parent_name=rp.parent.name, over_all_status=rp.overallStatus,
                                 cpu_expand_able_reservation=rp.summary.config.cpuAllocation.expandableReservation,
                                 cpu_reservation=rp.summary.config.cpuAllocation.reservation,
                                 cpu_limit=rp.summary.config.cpuAllocation.limit,
                                 cpu_shares=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_level=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_over_all_usage=rp.summary.runtime.cpu.overallUsage,
                                 cpu_max_usage=rp.summary.runtime.cpu.maxUsage,
                                 memory_expand_able_reservation=rp.summary.config.memoryAllocation.expandableReservation,
                                 memory_reservation=rp.summary.config.memoryAllocation.reservation,
                                 memory_limit=rp.summary.config.memoryAllocation.limit,
                                 memory_shares=rp.summary.config.memoryAllocation.shares.shares,
                                 memory_level=rp.summary.config.memoryAllocation.shares.level,
                                 memory_over_all_usage=rp.summary.runtime.memory.overallUsage,
                                 memory_max_usage=rp.summary.runtime.memory.maxUsage)

        db.instances.clean_all_vm_rp_name_by_rp_name(platform['id'], rp.name)
    print ('sync_rp_end:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))


def create_resource_pool(platform_id, dc_name, dc_mor_name, cluster_name,
                         cluster_mor_name, name, mor_name, parent_name, over_all_status,
                         cpu_expand_able_reservation,
                         cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage, cpu_max_usage,
                         memory_expand_able_reservation, memory_reservation, memory_limit, memory_shares, memory_level,
                         memory_over_all_usage, memory_max_usage):
    db.resource_pool.create_resource_pool(platform_id, dc_name, dc_mor_name, cluster_name, cluster_mor_name, name,
                                          mor_name, parent_name, over_all_status, cpu_expand_able_reservation,
                                          cpu_reservation, cpu_limit, cpu_shares,
                                          cpu_level, cpu_over_all_usage, cpu_max_usage, memory_expand_able_reservation,
                                          memory_reservation, memory_limit, memory_shares, memory_level,
                                          memory_over_all_usage, memory_max_usage)


def update_resource_pool(rp_id, platform_id, dc_name, cluster_name, cluster_mor_name, dc_mor_name, name, mor_name,
                         parent_name,
                         over_all_status, cpu_expand_able_reservation,
                         cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage, cpu_max_usage,
                         memory_expand_able_reservation, memory_reservation, memory_limit, memory_shares,
                         memory_level, memory_over_all_usage, memory_max_usage):
    db.resource_pool.update_resource_pool(rp_id, platform_id, dc_name, dc_mor_name, cluster_name, cluster_mor_name,
                                          name, mor_name, parent_name, over_all_status, cpu_expand_able_reservation,
                                          cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage,
                                          cpu_max_usage, memory_expand_able_reservation,
                                          memory_reservation, memory_limit, memory_shares, memory_level,
                                          memory_over_all_usage, memory_max_usage)


def get_resource_pool_list(platform_id, dc_mor_name, cluster_mor_name):
    results = db.resource_pool.get_resource_pool_list(platform_id, dc_mor_name, cluster_mor_name)

    resource_list = []
    for result in results:
        _t = {
            'id': result.id,
            'platform_id': result.platform_id,
            'dc_name': result.dc_name,
            'dc_mor_name': result.dc_mor_name,
            'cluster_name': result.cluster_name,
            'cluster_mor_name': result.cluster_mor_name,
            'name': result.name,
            'mor_name': result.mor_name,
            'parent_name': result.parent_name,
            'over_all_status': result.over_all_status,
            'cpu_expand_able_reservation': result.cpu_expand_able_reservation,
            'cpu_reservation': result.cpu_reservation,
            'cpu_limit': result.cpu_limit,
            'cpu_shares': result.cpu_shares,
            'cpu_level': result.cpu_level,
            'cpu_over_all_usage': result.cpu_over_all_usage,
            'cpu_max_usage': result.cpu_max_usage,
            'memory_expand_able_reservation': result.memory_expand_able_reservation,
            'memory_reservation': result.memory_reservation,
            'memory_limit': result.memory_limit,
            'memory_shares': result.memory_shares,
            'memory_level': result.memory_level,
            'memory_over_all_usage': result.memory_over_all_usage,
            'memory_max_usage': result.memory_max_usage
        }
        resource_list.append(_t)
    return resource_list
