# -*- coding=utf-8 -*-
from pyVim.task import WaitForTask
from pyVmomi import vim
from app.main.vcenter.control.instances import Instance
from app.main.vcenter.control.utils import get_mor_name
from app.main.vcenter import db


def create_datacenter(platform_id, dc_name, folder=None):
    instance = Instance(platform_id)
    si, content, platform = instance.si, instance.content, instance.platform
    # import pdb
    # pdb.set_trace()
    if len(dc_name) > 80:
        raise ValueError("The name of the datacenter must be under "
                         "80 characters.")
    if folder is None:
        folder = si.content.rootFolder
    if folder is not None and isinstance(folder, vim.Folder):
        folder.CreateDatacenter(name=dc_name)
    else:
        raise Exception('Failed to create datacenter')
    try:
        # 本地datacenters
        datacenters_list = db.datacenters.get_datacenters(platform_id)
        verify_list = []
        for datacenter in datacenters_list:
            verify_list.append(datacenter.mor_name)
        # 同步至本地
        datacenters = content.rootFolder.childEntity  # 获取平台datacenter数据
        for dc in datacenters:
            # print('pid:', vCenter_pid)
            result = db.vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)  # vcenter
            if result:
                pid = result.id
            else:
                pid = 1
            dc_mor = get_mor_name(dc)
            dc_host_moc = get_mor_name(dc.hostFolder)
            dc_vm_moc = get_mor_name(dc.vmFolder)
            del_name = db.datacenters.sync_datacenters(platform_id, dc.name, dc_mor, dc_host_moc, dc_vm_moc, pid)
            if del_name:
                verify_list.remove(dc_mor)
        # 删除本地多余的datacenter
        for dc_more in verify_list:
            db.datacenters.del_datacenter(platform_id, dc_more)
        return dc_name
    except Exception as e:
        pass


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
    dc = get_dc(platform_id, dc_id)
    dc_mor = get_mor_name(dc)
    # 任务销毁并等待
    task = dc.Destroy_Task()
    WaitForTask(task)
    # 删除本地数据库
    db.datacenters.del_datacenter(platform_id, dc_mor)

