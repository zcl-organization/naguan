# -*- coding=utf-8 -*-
from pyVim.task import WaitForTask
from pyVmomi import vim
from app.main.vcenter.control.instances import Instance
from app.main.vcenter.control.utils import get_mor_name
from app.main.vcenter import db
from app.main.vcenter.control.vcenter import sync_datacenter


def create_datacenter(platform_id, dc_name, folder=None):
    instance = Instance(platform_id)
    si, content, platform = instance.si, instance.content, instance.platform
    # import pdb
    # pdb.set_trace()
    if len(dc_name) > 80:
        raise ValueError("The name of the datacenter must be under "
                         "80 characters.")
    dc = db.datacenters.dc_name_if_exist(dc_name)
    if dc:
        raise ValueError('The datacenter name already exists')
    if folder is None:
        folder = si.content.rootFolder
    try:
        if folder is not None and isinstance(folder, vim.Folder):
            folder.CreateDatacenter(name=dc_name)
    except Exception as e:
        raise Exception('Failed to create datacenter. %s' % str(e))
    try:
        sync_datacenters(platform_id)
        return dc_name
    except Exception as e:
        raise Exception('sync datacenters fail. %s' % str(e))


# 根据id获取datacenter
def get_dc(platform_id, dc_id):
    instance = Instance(platform_id)
    si, content = instance.si, instance.content
    local_dc = db.datacenters.get_datacenter(dc_id)
    datacenters = content.rootFolder.childEntity
    for dc in datacenters:
        dc_mor = get_mor_name(dc)
        if dc_mor == local_dc.mor_name:
            return dc


def del_datacenter(platform_id, dc_id):
    # 判断本地datacenter下是否存在资源
    clusters_obj = db.datacenters.get_clusters_from_dc(platform_id, dc_id)
    if clusters_obj:
        raise Exception('Resources exist under the local datacenter, unable to delete')
    # 判断平台datacenter下是否存在资源
    instance_dc = get_dc(platform_id, dc_id)
    clusters = instance_dc.hostFolder.childEntity
    if clusters:
        # 同步数据至本地
        local_clusters = db.datacenters.get_clusters_from_dc2(platform_id, dc_id)
        vcenter_list = []
        for cluster in local_clusters:
            vcenter_list.append(cluster.id)
        instance = Instance(platform_id)
        si, content, platform = instance.si, instance.content, instance.platform
        sync_datacenter([instance_dc], si, content,
                        platform, vcenter_list, dc_id)
        raise Exception('Resources exist under the vCenter datacenter, unable to delete')

    dc = get_dc(platform_id, dc_id)
    dc_mor = get_mor_name(dc)
    # 任务销毁并等待
    task = dc.Destroy_Task()
    WaitForTask(task)
    # 删除本地数据库
    db.datacenters.del_datacenter(platform_id, dc_mor)


# 同步datacenter
def sync_datacenters(platform_id):
    instance = Instance(platform_id)
    content, platform = instance.content, instance.platform
    # 本地datacenters
    datacenters_list = db.datacenters.get_datacenters(platform_id)
    verify_list = []
    for datacenter in datacenters_list:
        verify_list.append(datacenter.mor_name)
    # 同步至本地
    datacenters = content.rootFolder.childEntity  # 获取平台datacenter数据
    for dc in datacenters:
        # print('pid:', vCenter_pid)
        result = db.vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)  # 判断vcenter
        if result:
            pid = result.id
        else:
            pid = 1
        dc_mor = get_mor_name(dc)
        dc_host_moc = get_mor_name(dc.hostFolder)
        dc_vm_moc = get_mor_name(dc.vmFolder)
        exist_name = db.datacenters.sync_datacenters(platform_id, dc.name, dc_mor, dc_host_moc, dc_vm_moc, pid)
        if exist_name:
            verify_list.remove(dc_mor)
    # 删除本地多余的datacenter
    for dc_more in verify_list:
        db.datacenters.del_datacenter(platform_id, dc_more)
