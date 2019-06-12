# -*- coding=utf-8 -*-
from pyVim.task import WaitForTask
from pyVmomi import vim
from app.main.vcenter.control.utils import get_mor_name, get_connect
from app.main.vcenter import db
from app.main.vcenter.control.vcenter import sync_vcenter_tree


def create_datacenter(platform_id, dc_name, folder=None):
    si, content, platform = get_connect(platform_id)

    if len(dc_name) > 80:
        raise ValueError("The name of the datacenter must be under "
                         "80 characters.")
    dc = db.datacenters.get_dc_name(dc_name)  # 根据是否存在同名dc
    if dc:
        raise ValueError('The datacenter name already exists')
    if folder is None:
        folder = si.content.rootFolder
    try:
        if folder is not None and isinstance(folder, vim.Folder):
            new_datacenter = folder.CreateDatacenter(name=dc_name)
            try:
                vCenter_pid = get_vCenter_pid(platform)
                dc_mor_name = get_mor_name(new_datacenter)
                dc_host_moc = get_mor_name(new_datacenter.hostFolder)
                dc_vm_moc = get_mor_name(new_datacenter.vmFolder)
                db.vcenter.vcenter_tree_create(tree_type=2, platform_id=platform_id, name=new_datacenter.name,
                                               dc_host_folder_mor_name=dc_host_moc,
                                               dc_mor_name=dc_mor_name, dc_oc_name=new_datacenter.name,
                                               dc_vm_folder_mor_name=dc_vm_moc, mor_name=dc_mor_name,
                                               cluster_mor_name=None, cluster_oc_name=None, pid=vCenter_pid)
                return dc_name
            except Exception as e:
                raise Exception('sync datacenters fail. %s' % str(e))
    except Exception as e:
        raise Exception('Failed to create datacenter. %s' % str(e))


# 根据id获取datacenter
def get_dc(platform_id, dc_id, content):
    local_dc = db.datacenters.get_datacenter_by_id(dc_id)
    datacenters = content.rootFolder.childEntity
    for dc in datacenters:
        dc_mor = get_mor_name(dc)
        if dc_mor == local_dc.mor_name:
            return dc


def del_datacenter(platform_id, dc_id):
    si, content, platform = get_connect(platform_id)

    # 判断本地datacenter下是否存在资源
    clusters_obj = db.datacenters.get_clusters_from_dc(platform_id, dc_id)
    if clusters_obj:
        raise Exception('Resources exist under the local datacenter, unable to delete')
    # 判断平台datacenter下是否存在资源
    instance_dc = get_dc(platform_id, dc_id, content)
    clusters = instance_dc.hostFolder.childEntity
    if clusters:
        # 同步数据至本地
        sync_vcenter_tree(si, content, platform)
        raise Exception('Resources exist under the vCenter datacenter, unable to delete')

    dc_mor = get_mor_name(instance_dc)
    # 任务销毁并等待
    task = instance_dc.Destroy_Task()
    WaitForTask(task)
    # 删除本地数据库
    db.datacenters.del_datacenter(platform_id, dc_mor)


# def sync_the_datacenter(platform_id, dc_id, instance_dc):
#     dc = db.datacenters.get_datacenter_by_id(dc_id)
#     dc_mor_name = dc.dc_mor_name
#
#     dc_and_child = db.datacenters.get_dc_and_child(platform_id, dc_mor_name)  #dc及其子资源
#     vcenter_list = []  # 待更新列表
#     for child in dc_and_child:
#         vcenter_list.append(child.id)
#     si, content, platform = get_connect(platform_id)
#
#     vCenter_pid = get_vCenter_pid(platform)
#     sync_datacenter([instance_dc], si, content, platform, vcenter_list, vCenter_pid)  # 同步datacenter


# 获取Vcenter id
def get_vCenter_pid(platform):
    result = db.vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)
    if result:
        vCenter_pid = result.id
    else:
        vCenter_pid = db.vcenter.vcenter_tree_create(tree_type=1, platform_id=platform['id'],
                                                     name=platform['platform_name'])
    return vCenter_pid