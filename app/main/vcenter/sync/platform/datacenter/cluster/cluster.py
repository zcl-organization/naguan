# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_clusters(platform_id, clusters):
    """
    同步一组集群
    """
    local_data = {
        item.mor_name: item.id for item in db.clusters.get_cluster_by_platform_id(platform_id)
    }

    for cluster in clusters:
        parent = cluster.parent.parent  # cluster.folder.datacenter
        sync_cluster(platform_id, cluster, parent)
        mor_name = get_mor_name(cluster)
        if mor_name in local_data.keys():
            local_data.pop(mor_name)
    
    for item in local_data.values():
        db.clusters.del_cluster(item)


def sync_cluster(platform_id, cluster, parent):
    """
    同步单个集群
    """
    cpu_sum, cpu_capacity, used_cpu = 0, 0, 0  # CPU数据 CPU核心数 CPU总频率 已使用量
    memory, used_memory = 0, 0  # 内存数据  总内存量  已使用内存量
    capacity, used_capacity = 0, 0  # 存储数据  总存储数据  已使用存储量
    vm_sum = 0  # 虚拟机数
    for host in cluster.host:
        cpu_num = int(host.summary.hardware.numCpuCores)
        cpu_sum += cpu_num
        cpu_capacity += cpu_num * host.summary.hardware.cpuMhz
        used_cpu += host.summary.quickStats.overallCpuUsage

        memory += host.summary.hardware.memorySize
        used_memory += host.summary.quickStats.overallMemoryUsage

        host_capcity, host_free_capacity = 0, 0
        for datastore in host.datastore:
            host_capcity += datastore.summary.capacity
            host_free_capacity += datastore.summary.freeSpace
        capacity += host_capcity
        used_capacity += host_capcity - host_free_capacity

        vm_sum += len(host.vm)

    data = dict(
        name=cluster.name,
        mor_name=get_mor_name(cluster),
        platform_id=platform_id,
        dc_name=parent.name,
        dc_mor_name=get_mor_name(parent),
        cpu_nums=cpu_sum,
        cpu_capacity=cpu_capacity,
        used_cpu=used_cpu,
        memory=memory,
        used_memory=used_memory,
        capacity=capacity,
        used_capacity=used_capacity,
        host_nums=len(cluster.host),
        vm_nums=vm_sum
    )

    cluster_info = db.clusters.get_cluster_by_mor_name(platform_id, get_mor_name(cluster))
    if cluster_info:
        cluster_local = db.clusters.update_cluster(**data)
    else:
        cluster_local = db.clusters.create_cluster(**data)

    return cluster_local