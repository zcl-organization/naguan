# -*- coding=utf-8 -*-
from pyVmomi import vim
from pyVim.task import WaitForTask
from app.main.vcenter.control.datacenters import get_dc
from app.main.vcenter import db
from app.main.vcenter.control.instances import Instance
from app.main.vcenter.control.utils import get_mor_name


def create_cluster(platform_id, dc_id, cluster_name, cluster_spec=None):
    """
    Method to create a Cluster in vCenter
    :param kwargs:
    :return: Cluster MORef
    """
    instance_dc = get_dc(platform_id, dc_id)
    instance = Instance(platform_id)
    content = instance.content
    if instance_dc is None:
        raise ValueError("Missing value for datacenter.")
    if cluster_name is None:
        raise ValueError("Missing value for name.")
    if cluster_spec is None:
        cluster_spec = vim.cluster.ConfigSpecEx()

    host_folder = instance_dc.hostFolder
    cluster = host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)
    try:
        cluster_mor_name = get_mor_name(cluster)
        # 获取datacenter对象
        dc_obj = db.datacenters.get_datacenter(dc_id)
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
        pass
    return cluster_name


def del_cluster(platform_id, dc_id, cluster_name):
    instance_dc = get_dc(platform_id, dc_id)
    clusters = instance_dc.hostFolder.childEntity
    for cluster in clusters:
        if cluster.name == cluster_name:
            task = cluster.Destroy_Task()
            WaitForTask(task)

