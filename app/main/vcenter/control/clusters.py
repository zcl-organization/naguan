# -*- coding=utf-8 -*-
from flask import g
from pyVmomi import vim
from pyVim.task import WaitForTask
from app.main.vcenter import db
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.control.utils import get_mor_name, get_connect, get_obj, get_obj_by_mor_name


def sync_cluster(vcenter_obj, dc_obj, cluster_obj):
    cluster_mor_name = get_mor_name(cluster_obj)
    dc_mor_name = get_mor_name(dc_obj)
    dc_host_moc = get_mor_name(dc_obj.hostFolder)
    dc_vm_moc = get_mor_name(dc_obj.vmFolder)

    # 获取本地tree_datacenter对象
    tree_dc = db.vcenter.get_vcenter_obj_by_mor_name(vcenter_obj.platform['id'], dc_mor_name)

    # 判断集群是否存在
    tree_cluster_info = db.vcenter.vcenter_tree_get_by_cluster(vcenter_obj.platform['id'], cluster_mor_name, 3)
    if tree_cluster_info:
        cluster_tree = db.vcenter.vcenter_tree_update(tree_type=3, platform_id=vcenter_obj.platform['id'],
                                                      name=cluster_obj.name, dc_mor_name=dc_mor_name,
                                                      dc_oc_name=dc_obj.name, mor_name=cluster_mor_name,
                                                      dc_host_folder_mor_name=dc_host_moc,
                                                      dc_vm_folder_mor_name=dc_vm_moc,
                                                      cluster_mor_name=cluster_mor_name,
                                                      cluster_oc_name=cluster_obj.name,
                                                      pid=tree_dc.id)
    else:
        cluster_tree = db.vcenter.vcenter_tree_create(tree_type=3, platform_id=vcenter_obj.platform['id'],
                                                      name=cluster_obj.name,
                                                      dc_mor_name=dc_mor_name, dc_oc_name=dc_obj.name,
                                                      mor_name=cluster_mor_name,
                                                      dc_host_folder_mor_name=dc_host_moc,
                                                      dc_vm_folder_mor_name=dc_vm_moc,
                                                      cluster_mor_name=cluster_mor_name,
                                                      cluster_oc_name=cluster_obj.name, pid=tree_dc.id)
    # 本地clusters同步
    cpu_nums = 0
    cpu_capacity = 0
    used_cpu = 0
    memory = 0
    used_memory = 0
    capacity = 0
    used_capacity = 0
    vm_nums = 0
    host_nums = 0
    if len(cluster_obj.host) > 0:
        for host in cluster_obj.host:
            nums = int(host.summary.hardware.numCpuCores)
            cpu_nums += nums
            cpu_capacity += nums * host.summary.hardware.cpuMhz
            used_cpu += host.summary.quickStats.overallCpuUsage
            memory += host.summary.hardware.memorySize
            used_memory += host.summary.quickStats.overallMemoryUsage
            host_capacity = 0
            host_free_capacity = 0
            for ds in host.datastore:
                host_capacity += ds.summary.capacity
                host_free_capacity += ds.summary.freeSpace
            host_used_capacity = host_capacity - host_free_capacity
            capacity += host_capacity
            used_capacity += host_used_capacity
            vm_nums += len(host.vm)
        host_nums = len(cluster_obj.host)
    data = dict(
        name=cluster_obj.name, mor_name=cluster_mor_name, platform_id=vCenter_obj.platform['id'],
        dc_name=dc_obj.name, dc_mor_name=dc_mor_name, cpu_nums=cpu_nums, cpu_capacity=cpu_capacity,
        used_cpu=used_cpu, memory=memory, used_memory=used_memory, capacity=capacity,
        used_capacity=used_capacity, host_nums=host_nums, vm_nums=vm_nums
    )
    # 获取本地cluster对象
    cluster_info = db.clusters.get_cluster_by_mor_name(vcenter_obj.platform['id'], cluster_mor_name)
    if cluster_info:
        cluster_local = db.clusters.update_cluster(**data)
    else:
        cluster_local = db.clusters.create_cluster(**data)

    return cluster_tree, cluster_local


"""
def create_cluster(platform_id, dc_id, cluster_name, cluster_spec=None):

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
                                                    dc_mor_name=vcenter_tree_dc.mor_name,
                                                    dc_oc_name=vcenter_tree_dc.name,
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

"""


class Cluster(object):
    def __init__(self, platform_id):
        self._platform_id = platform_id
        self._vCenter = VCenter(platform_id)

    def create(self, dc_id, cluster_name):
        dc_local = db.datacenters.get_dc_by_id(dc_id)

        dc_obj = get_obj(self._vCenter.connect, [vim.Datacenter], dc_local.name)
        if dc_obj is None:
            g.error_code = 4103
            raise ValueError("Missing value for datacenter.")

        # 判断dc下是否存在同名cluster
        cluster_local = db.clusters.get_cluster_by_name(self._vCenter.platform['id'], dc_local.name, cluster_name)
        if cluster_local:
            g.error_code = 4105
            raise ValueError('The cluster name already exists')

        cluster_spec = vim.cluster.ConfigSpecEx()
        host_folder = dc_obj.hostFolder
        try:
            new_cluster = host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)
        except RuntimeError:
            raise Exception('task to create cluster failed')
        # datacenters = self._vCenter.connect.rootFolder.childEntity
        # for dc in datacenters:
        #     for cluster in dc.hostFolder.childEntity:
        #         sync_cluster(vCenter_obj=self._vCenter, dc_obj=dc, cluster_obj=cluster)
        cluster_tree, cluster_local = sync_cluster(vcenter_obj=self._vCenter, dc_obj=dc_obj, cluster_obj=new_cluster)
        return cluster_local

    def delete(self, platform_id, cluster_id):
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

    def list(self, platform_id=None, cluster_id=None, cluster_name=None, dc_name=None):
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
