# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_hosts(platform_id, hosts):
    """
    同步所有主机
    获取 -> 处理 -> 回收
    """
    local_data = {
        item.mor_name: item.id for item in db.host.get_host_by_data(platform_id=platform_id)
    }

    for host in hosts:
        parent = host.parent
        sync_host(platform_id, host, parent)
        host_mor_name = get_mor_name(host)
        if host_mor_name in local_data.keys():
            local_data.pop(host_mor_name)
        
    for name, host_id in local_data.items():
        db.host.del_host_by_id(host_id)


def sync_host(platform_id, host, parent):
    """
    同步单个主机
    """
    capacity, free_capacity = 0, 0
    for ds in host.datastore:
        capacity += ds.summary.capacity
        free_capacity += ds.summary.freeSpace
    
    data = dict(
        name=host.summary.config.name, 
        mor_mame=get_mor_name(host), 
        dc_name=parent.parent.parent.name,  # cluster.folder.datacenter
        dc_mor_name=get_mor_name(parent.parent.parent),  # cluster.folder.datacenter
        cluster_name=parent.name,
        cluster_mor_name=get_mor_name(parent), 
        port=host.summary.config.port,
        power_state=str(host.summary.runtime.powerState), 
        connection_state=str(host.summary.runtime.connectionState),
        maintenance_mode=host.summary.runtime.inMaintenanceMode, 
        platform_id=platform_id,
        uuid=host.summary.hardware.uuid, 
        cpu_cores=int(host.summary.hardware.numCpuCores),
        memory=host.summary.hardware.memorySize, 
        used_memory=host.summary.quickStats.overallMemoryUsage,
        capacity=capacity, 
        used_capacity=capacity - free_capacity, 
        used_cpu=host.summary.quickStats.overallCpuUsage,
        cpu_mhz=host.summary.hardware.cpuMhz, 
        cpu_model=host.summary.hardware.cpuModel,
        version=host.summary.config.product.version, 
        image=host.summary.config.product.name, 
        build=host.summary.config.product.build,
        full_name=host.summary.config.product.fullName, 
        boot_time=host.summary.runtime.bootTime.strftime('%Y-%m-%d %H:%M:%S'),
        uptime=host.summary.quickStats.uptime, 
        vm_nums=len(host.vm), 
        network_nums=len(host.network)
    )

    host_info = db.host.get_host_by_mor_name(platform_id, get_mor_name(host))
    if host_info:
        db.host.update_host(**data)   # 更新的查询部分可能有问题
    else:
        db.host.add_host(**data)
