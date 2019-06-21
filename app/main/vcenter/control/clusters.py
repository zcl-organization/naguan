# -*- coding=utf-8 -*-
from flask import g
from pyVmomi import vim
from pyVim.task import WaitForTask
from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name, get_connect, get_obj, get_obj_by_mor_name


def create_cluster(platform_id, dc_id, cluster_name, cluster_spec=None):
    """
    Method to create a Cluster in vCenter
    :param kwargs:
    :return: Cluster MORef
    """
    si, content, platform = get_connect(platform_id)
    # 本地dc
    dc = db.datacenters.get_dc_by_id(dc_id)
    # dc对象

    dc_obj = get_obj(content, [vim.Datacenter], dc.name)
    if dc_obj is None:
        g.error_code = 4103
        raise ValueError("Missing value for datacenter.")
    if cluster_name is None:
        g.error_code = 4104
        raise ValueError("Missing value for name.")
    if cluster_spec is None:
        cluster_spec = vim.cluster.ConfigSpecEx()
    # 判断dc下是否存在同名cluster
    local_cluster = db.clusters.get_cluster_by_name(platform_id, dc.name, cluster_name)
    if local_cluster:
        g.error_code = 4105
        raise ValueError('The cluster name already exists')

    host_folder = dc_obj.hostFolder
    cluster = host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)

    # 同步至本地
    try:
        cluster_mor_name = get_mor_name(cluster)
        # 获取本地datacenter对象
        vcenter_tree_dc = db.vcenter.get_vcenter_obj_by_mor_name(platform_id, dc.mor_name)
        # 本地vcenter_tree同步
        cluster_id = db.vcenter.vcenter_tree_create(tree_type=3, platform_id=platform_id, name=cluster_name,
                                                    dc_host_folder_mor_name=vcenter_tree_dc.dc_host_folder_mor_name,
                                                    dc_mor_name=vcenter_tree_dc.mor_name, dc_oc_name=vcenter_tree_dc.name,
                                                    dc_vm_folder_mor_name=vcenter_tree_dc.dc_vm_folder_mor_name,
                                                    mor_name=cluster_mor_name, cluster_mor_name=cluster_mor_name,
                                                    cluster_oc_name=cluster_name, pid=vcenter_tree_dc.id)
        # 本地clusters同步
        data = dict(
            name=cluster_name, mor_name=cluster_mor_name, platform_id=platform_id, dc_name=vcenter_tree_dc.name,
            dc_mor_name=vcenter_tree_dc.mor_name, cpu_nums=0, cpu_capacity=0, used_cpu=0, memory=0, used_memory=0,
            capacity=0, used_capacity=0, host_nums=0, vm_nums=0
        )
        new_cluster_id = db.clusters.create_cluster(**data)
        rp_obj = content.viewManager.CreateContainerView(cluster, [vim.ResourcePool], True)
        rps = rp_obj.view
        for rp in rps:
            rp_mor = get_mor_name(rp)
            # 创建本地数据库resource
            db.vcenter.vcenter_tree_create(tree_type=5, platform_id=platform_id, name=rp.name,
                                           dc_host_folder_mor_name=vcenter_tree_dc.dc_host_folder_mor_name,
                                           dc_mor_name=vcenter_tree_dc.dc_mor_name, dc_oc_name=vcenter_tree_dc.name,
                                           dc_vm_folder_mor_name=vcenter_tree_dc.dc_vm_folder_mor_name,
                                           mor_name=rp_mor, cluster_mor_name=cluster_mor_name,
                                           cluster_oc_name=cluster_name, pid=cluster_id)
        return new_cluster_id
    except Exception as e:
        raise Exception('Failed to create cluster. %s' % str(e))


def del_cluster(platform_id, cluster_id):
    cluster = db.clusters.get_cluster(platform_id, cluster_id)
    if not cluster:
        g.error_code = 4154
        raise Exception('Cluster_id error, please confirm before deleting')
    # 判断本地cluster下是否存在资源
    cluster_mor_name = cluster.mor_name
    cluster_resource = db.vcenter.get_cluster_and_cluster_resource(platform_id, cluster_mor_name)  # 集群及其下的资源
    if len(cluster_resource) > 2:  # 本地校验
        g.error_code = 4155
        raise Exception('Resources exist under the local cluster, unable to delete')

    vcenter_tree_cluster = db.vcenter.get_vcenter_obj_by_mor_name(platform_id, cluster_mor_name)
    dc_id = vcenter_tree_cluster.pid
    si, content, platform = get_connect(platform_id)

    dc = db.vcenter.get_datacenter_by_id(dc_id)
    dc_obj = get_obj(content, [vim.Datacenter], dc.name)
    # 平台实例
    cluster_obj = get_obj_by_mor_name(content, [vim.ClusterComputeResource], cluster.mor_name)
    rp_obj = content.viewManager.CreateContainerView(cluster_obj, [vim.ResourcePool], True)
    resourcepools = rp_obj.view
    if len(resourcepools) > 1:
        g.error_code = 4156
        raise Exception('Resources exist under the vCenter cluster, unable to delete')

    clusters = dc_obj.hostFolder.childEntity
    cluster_name = cluster_obj.name
    for cluster in clusters:
        if cluster.name == cluster_name:
            hosts = cluster.host
            if hosts:  # 当cluster下存在host时
                # sync_vcenter_tree(si, content, platform)
                g.error_code = 4156
                raise Exception('Resources exist under the vCenter datacenter, unable to delete')
            else:
                task = cluster.Destroy_Task()
                WaitForTask(task)
                # vcenter_tree 删除
                for cluster in cluster_resource:
                    db.vcenter.vcenter_tree_delete_by_id(cluster.id)
                # cluster删除
                db.clusters.del_cluster(cluster_id)
                return 'Del cluster success'
    else:
        raise Exception('No exist cluster.')


def find_clusters(platform_id=None, cluster_id=None, cluster_name=None, dc_name=None):
    clusters = db.clusters.find_clusters(platform_id, cluster_id, cluster_name, dc_name)
    cluster_list = []
    for cluster in clusters:
        data = dict(
            id=cluster.id, name=cluster.name, mor_name=cluster.mor_name, platform_id=cluster.platform_id,
            dc_name=cluster.dc_name, dc_mor_name=cluster.dc_mor_name, cpu_nums=cluster.cpu_nums,
            cpu_capacity=cluster.cpu_capacity, used_cpu=cluster.used_cpu, memory=cluster.memory,
            used_memory=cluster.used_memory, capacity=cluster.capacity, used_capacity=cluster.used_capacity,
            host_nums=cluster.host_nums, vm_nums=cluster.vm_nums,
        )
        cluster_list.append(data)
    return cluster_list
