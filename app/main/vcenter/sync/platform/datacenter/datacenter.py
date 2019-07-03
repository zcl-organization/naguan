# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_datacenters(platform_id, datacenters):
    """
    同步所有DC数据
    获取 -> 处理 -> 回收
    """
    dc_datas = db.datacenters.get_datacenter_by_platform_id(platform_id)
    local_data = {item.mor_name: item.id for item in dc_datas}

    for datacenter in datacenters:
        result = sync_datacenter(platform_id, datacenter)
        if result.mor_name in local_data.keys():
            local_data.pop(result.mor_name)

    for item in local_data.values():
        db.datacenters.del_datacenter(item)


def sync_datacenter(platform_id, datacenter):
    """
    处理单个DC数据
    TODO 数据收集待优化
    """
    dc_mor_name = get_mor_name(datacenter)

    vm_nums = 0  # VM数量统计
    for data in datacenter.vmFolder.childEntity:
        if isinstance(data, vim.VirtualMachine):
            vm_nums += 1

    host_nums = 0  # 主机数量
    cpu_capacity, used_cpu = 0, 0  # CPU数据
    memory, used_memory = 0, 0  # 内存数据
    capacity, used_capacity = 0, 0  # 容量数据
    for cluster in datacenter.hostFolder.childEntity:
        host_nums += len(cluster.host)
        for host in cluster.host:
            cpu_capacity += int(host.summary.hardware.numCpuCores) * host.summary.hardware.cpuMhz
            used_cpu += host.summary.quickStats.overallCpuUsage
            memory += host.summary.hardware.memorySize
            used_memory += host.summary.quickStats.overallMemoryUsage
            host_capacity, host_free_capacity = 0, 0
            for ds in host.datastore:
                host_capacity += ds.summary.capacity
                host_free_capacity += ds.summary.freeSpace
            capacity += host_capacity
            used_capacity += host_capacity - host_free_capacity

    dc_data = dict(
        name=datacenter.name,
        mor_name=dc_mor_name, 
        platform_id=platform_id,
        host_nums=host_nums, 
        vm_nums=vm_nums, 
        cluster_nums=len(datacenter.hostFolder.childEntity),
        network_nums=len(datacenter.network), 
        datastore_nums=len(datacenter.datastore),
        cpu_capacity=cpu_capacity, 
        used_cpu=used_cpu, 
        memory=memory,
        used_memory=used_memory, 
        capacity=capacity, 
        used_capacity=used_capacity,
    )

    dc_info = db.datacenters.get_datacenter_by_mor_name(platform_id, dc_mor_name)
    if dc_info:
        dc_local = db.datacenters.update_datacenter(**dc_data)
    else:
        dc_local = db.datacenters.create_datacenter(**dc_data)
    
    return dc_local
