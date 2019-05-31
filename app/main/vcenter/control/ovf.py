# -*- coding:utf-8 -*-
from app.main.vcenter.control.utils import get_connect
from pyVmomi import vim


def ovf_list():
    si, content, platform = get_connect(1)

    ovf_manager = si.content.ovfManager
    ovf_descriptor = None
    print(1)
    ovf_object = ovf_manager.ParseDescriptor(ovf_descriptor, vim.OvfManager.ParseDescriptorParams())
    print(2)
    print(ovf_object)
