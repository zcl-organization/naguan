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
            new_datacenter = folder.CreateDatacenter(name=dc_name)
            try:
                result = db.vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)
                if result:
                    vCenter_pid = result.id
                else:
                    vCenter_pid = 1
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
        sync_the_datacenter(platform_id, dc_id, instance_dc)
        raise Exception('Resources exist under the vCenter datacenter, unable to delete')

    dc_mor = get_mor_name(instance_dc)
    # 任务销毁并等待
    task = instance_dc.Destroy_Task()
    WaitForTask(task)
    # 删除本地数据库
    db.datacenters.del_datacenter(platform_id, dc_mor)


def sync_the_datacenter(platform_id, dc_id, instance_dc):
    dc = db.datacenters.get_datacenter(dc_id)
    dc_mor_name = dc.dc_mor_name
    dc_and_child = db.datacenters.get_dc_and_its(platform_id, dc_mor_name)  #
    vcenter_list = []
    for child in dc_and_child:
        vcenter_list.append(child.id)
    instance = Instance(platform_id)
    si, content, platform = instance.si, instance.content, instance.platform
    sync_datacenter([instance_dc], si, content, platform, vcenter_list, dc_id)

