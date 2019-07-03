# -*- coding: utf-8 -*-
"""
TODO 优化待处理
为了避开丑陋的四五级for操作，编写了一组函数假装隐藏了丑陋的写法。
可能导致过度封装 （逃～）
"""
from pyVmomi import vim

from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.sync.const import SyncOperation
from app.main.vcenter.sync.const import PlatformType


def get_obj(content, folder, vim_type):
    return content.viewManager.CreateContainerView(folder, vim_type, True).view


def sync_info(platform_id):
    """
    拍平同步数据, 只做收集！！！
    """
    vcenter = VCenter(platform_id)
    connect = vcenter.connect

    result_info = {}

    result_info.setdefault(SyncOperation.PLATFORM, []).append(
        (PlatformType.PLATFROM, vcenter.platform['name'])
    )

    for datacenter in connect.rootFolder.childEntity:
        result_info.setdefault(SyncOperation.PLATFORM, []).append(
            (PlatformType.DATACENTER, datacenter)
        )
        result_info.setdefault(SyncOperation.DATACENTER, []).append(datacenter)

        _flat_portgroup(result_info, datacenter.network, platform_id)

        network_folder = datacenter.networkFolder.childEntity
        _flat_dvswitch(result_info, network_folder, platform_id)
            
        datastores = get_obj(connect, datacenter, [vim.Datastore])
        _flat_datastore(result_info, datastores, platform_id)

        cluster_folder = datacenter.hostFolder.childEntity
        _flat_cluster(result_info, cluster_folder, platform_id, connect)

    return result_info


def _flat_portgroup(result_info, network_portgroups, platform_id):
    """
    拍平端口组数据
    """
    for portgroup in network_portgroups:
        result_info.setdefault(SyncOperation.PORTGROUP, []).append(portgroup)


def _flat_dvswitch(result_info, network_folder, platform_id):
    """
    拍平DVSwitch及其子项
    """
    for dvs in network_folder:
        if isinstance(dvs, vim.dvs.VmwareDistributedVirtualSwitch):
            result_info.setdefault(SyncOperation.DVSWITCH, []).append(dvs)


def _flat_datastore(result_info, datastores, platform_id):
    """
    拍平datastore及其子项
    """
    for ds in datastores:
        result_info.setdefault(SyncOperation.DATASTORE, []).append(ds)


def _flat_cluster(result_info, cluster_folder, platform_id, connect):
    """
    拍平集群及其子项
    """
    for cluster in cluster_folder:
        result_info.setdefault(SyncOperation.PLATFORM, []).append(
            (PlatformType.CLUSTER, cluster)
        )
        result_info.setdefault(SyncOperation.CLUSTER, []).append(cluster)

        resource_pools = get_obj(connect, cluster, [vim.ResourcePool])
        _flat_cluster_resourcepool(result_info, resource_pools, platform_id)
        
        _flat_cluster_host(result_info, cluster.host, platform_id)


def _flat_cluster_resourcepool(result_info, resource_pools, platform_id):
    """
    拍平资源池及其子项
    """
    for rp in resource_pools:
        result_info.setdefault(SyncOperation.PLATFORM, []).append(
            (PlatformType.RESOURCEPOOL, rp)
        )
        result_info.setdefault(SyncOperation.RESOURCEPOOL, []).append(rp)


def _flat_cluster_host(result_info, hosts, platform_id):
    """
    拍平主机及其子项
    """
    for host in hosts:
        result_info.setdefault(SyncOperation.PLATFORM, []).append(
            (PlatformType.HOST, host)
        )
        result_info.setdefault(SyncOperation.HOST, []).append(host)
        
        vswitchs = host.configManager.networkSystem.networkInfo.vswitch 
        _flat_cluster_host_vswitch(result_info, vswitchs, platform_id, host)

        _flat_cluster_host_vm(result_info, host.vm, platform_id)


def _flat_cluster_host_vswitch(result_info, vswitchs, platform_id, host):
    """
    拍平vswitch及其子项
    """
    for vs in vswitchs:
        result_info.setdefault(SyncOperation.VSWITCH, []).append((vs, host))


def _flat_cluster_host_vm(result_info, vms, platform_id):
    """
    拍平VM及其子项
    """
    for vm in vms:
        result_info.setdefault(SyncOperation.VM, []).append(vm)
