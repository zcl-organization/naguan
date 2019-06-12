# -*- coding=utf-8 -*-
from pyVmomi import vim
from pyVim.task import WaitForTask
from app.main.vcenter.control.datacenters import get_dc
from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name, get_connect
from app.main.vcenter.control.vcenter import sync_vcenter_tree


def create_cluster(platform_id, dc_id, cluster_name, cluster_spec=None):
    """
    Method to create a Cluster in vCenter
    :param kwargs:
    :return: Cluster MORef
    """
    si, content, platform = get_connect(platform_id)
    instance_dc = get_dc(platform_id, dc_id, content)
    if instance_dc is None:
        raise ValueError("Missing value for datacenter.")
    if cluster_name is None:
        raise ValueError("Missing value for name.")
    if cluster_spec is None:
        cluster_spec = vim.cluster.ConfigSpecEx()
    local_cluster = db.clusters.get_cluster_by_name(platform_id, dc_id, cluster_name)
    if local_cluster:
        raise ValueError('The cluster name already exists')

    host_folder = instance_dc.hostFolder
    cluster = host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)

    # 同步至本地
    try:
        cluster_mor_name = get_mor_name(cluster)
        # 获取datacenter对象
        dc_obj = db.datacenters.get_datacenter_by_id(dc_id)
        # 创建本地cluster
        cluster_id = db.vcenter.vcenter_tree_create(tree_type=3, platform_id=platform_id, name=cluster_name,
                                                    dc_host_folder_mor_name=dc_obj.dc_host_folder_mor_name,
                                                    dc_mor_name=dc_obj.dc_mor_name, dc_oc_name=dc_obj.name,
                                                    dc_vm_folder_mor_name=dc_obj.dc_vm_folder_mor_name,
                                                    mor_name=cluster_mor_name, cluster_mor_name=cluster_mor_name,
                                                    cluster_oc_name=cluster_name, pid=dc_id)

        rp_obj = content.viewManager.CreateContainerView(cluster, [vim.ResourcePool], True)
        rps = rp_obj.view
        for rp in rps:
            rp_mor = get_mor_name(rp)
            # 创建本地数据库resource
            db.vcenter.vcenter_tree_create(tree_type=5, platform_id=platform_id, name=rp.name,
                                           dc_host_folder_mor_name=dc_obj.dc_host_folder_mor_name,
                                           dc_mor_name=dc_obj.dc_mor_name, dc_oc_name=dc_obj.name,
                                           dc_vm_folder_mor_name=dc_obj.dc_vm_folder_mor_name,
                                           mor_name=rp_mor, cluster_mor_name=cluster_mor_name,
                                           cluster_oc_name=cluster_name, pid=cluster_id)
    except Exception as e:
        raise Exception('Failed to create cluster. %s' % str(e))
    return cluster_name


def del_cluster(platform_id, cluster_id):
    # 判断本地cluster下是否存在资源
    cluster_obj = db.clusters.get_cluster_mor_name(platform_id, cluster_id)
    if not cluster_obj:
        raise Exception('Cluster_id error, please confirm before deleting')
    cluster_mor_name = cluster_obj.mor_name
    cluster_resource = db.clusters.get_cluster_cluster_resource(platform_id, cluster_mor_name)  # 集群及其下的资源
    if len(cluster_resource) > 2:  # 本地校验
        raise Exception('Resources exist under the local datacenter, unable to delete')

    dc_id = cluster_obj.pid
    si, content, platform = get_connect(platform_id)

    instance_dc = get_dc(platform_id, dc_id, content)

    obj = content.viewManager.CreateContainerView(instance_dc, [vim.ResourcePool], True)
    resourcepools = obj.view
    for rp in resourcepools:
        if rp.parent.parent.name == cluster_obj.name:  # 当cluster下存在资源池时
            sync_vcenter_tree(si, content, platform)
            raise Exception('Resources exist under the vCenter datacenter, unable to delete')

    clusters = instance_dc.hostFolder.childEntity
    cluster_name = cluster_obj.name
    for cluster in clusters:
        if cluster.name == cluster_name:
            hosts = cluster.host
            if hosts:  # 当cluster下存在host时
                sync_vcenter_tree(si, content, platform)
                raise Exception('Resources exist under the vCenter datacenter, unable to delete')
            else:
                task = cluster.Destroy_Task()
                WaitForTask(task)
                for cluster in cluster_resource:
                    db.vcenter.vcenter_tree_del_cluster(cluster.id)
                return 'Del cluster success'
    else:
        raise Exception('No exist cluster.')



