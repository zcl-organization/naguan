# -*- coding:utf-8 -*-
from flask_restful.representations import json
from pyVim import connect
import atexit

from pyVmomi import vmodl
from pyVmomi import vim

from app.main.vcenter.control.vcenter import get_connect, vcenter_tree_list


def sizeof_fmt(num):
    """
    Returns the human readable version of a file size
    :param num:
    :return:
    """
    for item in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def get_largest_free_rp(si, dc):
    """
    Get the resource pool with the largest unreserved memory for VMs.
    """
    viewManager = si.content.viewManager
    containerView = viewManager.CreateContainerView(dc, [vim.ResourcePool],
                                                    True)
    largestRp = None
    unreservedForVm = 0
    try:
        for rp in containerView.view:
            if rp.runtime.memory.unreservedForVm > unreservedForVm:
                largestRp = rp
                unreservedForVm = rp.runtime.memory.unreservedForVm
    finally:
        containerView.Destroy()
    if largestRp is None:
        raise Exception("Failed to find a resource pool in dc %s" % dc.name)
    return largestRp


def test_get_ds(platform_id):
    s, content, platform = get_connect(platform_id)

    # obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)

    datacenters_object_view = content.viewManager.CreateContainerView(
        content.rootFolder,
        [vim.Datacenter],
        True)

    for dc in datacenters_object_view.view:

        obj = content.viewManager.CreateContainerView(dc,
                                                      [vim.Datastore],
                                                      True)


        # manage.filesView
        # # 获取资源池
        # rp = get_largest_free_rp(s, dc)
        # print (dir(rp.summary))

        # return 'cccc'
        datastores = obj.view

        for ds in datastores:
            # print(dir(ds))
            # print(ds.folder)


            # print(browse)
            # Folder = content.viewManager.CreateContainerView(dc,
            #                                                  [vim.Folder],
            #                                                  True)

            # print(Folder.view)

            # folders = Folder.view

            # for folder in folders:
            #     print (folder.name)
            # print (ds.parent.name)
            # print(dir(ds))
            # print(ds.host.summary.name)

            ds_capacity = ds.summary.capacity
            ds_freespace = ds.summary.freeSpace
            ds_uncommitted = ds.summary.uncommitted if ds.summary.uncommitted else 0
            ds_provisioned = ds_capacity - ds_freespace + ds_uncommitted
            ds_overp = ds_provisioned - ds_capacity
            ds_overp_pct = (ds_overp * 100) / ds_capacity \
                if ds_capacity else 0
            print('dc:', dc.name, 'version:', ds.info.name)
            print('dc:', dc.name, 'capacity:', sizeof_fmt(ds_capacity))
            print('dc:', dc.name, 'freeSpace:', sizeof_fmt(ds_freespace))
            print('dc:', dc.name, 'ds_uncommitted :', sizeof_fmt(ds_uncommitted))
            print('dc:', dc.name, 'ds_provisioned ', sizeof_fmt(ds_provisioned))

            # print('name:', ds.info.name)
            # print('type:', ds.info.type)
            # print('ssd:', ds.info.ssd)
            # print('ssd:', ds.info.ssd)
            # print('local:', ds.info.local)
            # print(dir(ds.summary.capacity))
