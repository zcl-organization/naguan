# -*- coding=utf-8 -*-
from pyVmomi import vim
from app.main.vcenter.control.instances import Instance
from app.main.vcenter.control.utils import get_mor_name
from app.main.vcenter import db


def create_datacenter(platform_id, dc_name, folder=None):
    instance = Instance(platform_id)
    si, content, platform = instance.si, instance.content, instance.platform

    if len(dc_name) > 79:
        raise ValueError("The name of the datacenter must be under "
                         "80 characters.")
    if folder is None:
        folder = si.content.rootFolder
    # if folder is not None and isinstance(folder, vim.Folder):
    #     dc_moref = folder.CreateDatacenter(name=dc_name)

    else:
        raise Exception('Failed to create datacenter')
    try:
        # 本地datacenters
        datacenters_list = db.datacenters.get_datacenters(platform_id)
        verify_list = []
        for datacenter in datacenters_list:
            verify_list.append(datacenter.name)
        # 同步至本地
        datacenters = content.rootFolder.childEntity
        for dc in datacenters:
            # print('pid:', vCenter_pid)
            dc_mor = get_mor_name(dc)
            dc_host_moc = get_mor_name(dc.hostFolder)
            dc_vm_moc = get_mor_name(dc.vmFolder)
            db.datacenters.sync_datacenters(platform_id, dc.name, dc_mor, dc_host_moc, dc_vm_moc)

        return dc_moref
    except Exception as e:
        pass
