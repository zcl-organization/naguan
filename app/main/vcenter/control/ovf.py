# -*- coding:utf-8 -*-
from app.main.vcenter.control.utils import get_connect
from pyVmomi import vim


def ovf_list():
    si, content, platform = get_connect(1)
    dcs = content.rootFolder.childEntity
    for dc_itme in dcs:
        ds_obj = content.viewManager.CreateContainerView(dc_itme, [vim.Datastore], True)
        dss = ds_obj.view
        # print(dss)
        for dc_item in dss:
            ovf_obj = content.viewManager.CreateContainerView(dc_item, [vim.OvfFile], True)
            ovf = ovf_obj.view
            print ovf
    #
    # ovf_manager = si.content.ovfManager
    # ovf_descriptor = None
    # print(1)
    # ovf_object = ovf_manager.ParseDescriptor(ovf_descriptor, vim.OvfManager.ParseDescriptorParams())
    # print(2)
    # print(ovf_object)
