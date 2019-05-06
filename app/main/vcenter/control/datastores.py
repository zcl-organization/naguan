# -*- coding:utf-8 -*-
from flask_restful.representations import json
from pyVim import connect
import atexit

from pyVmomi import vmodl
from pyVmomi import vim

# from app.main.vcenter.control import get_connect
from app.main.vcenter.control.utils import get_connect, get_mor_name
# from app.main.vcenter.control.vcenter import vcenter_tree_list
from app.main.vcenter import db
from app.main.vcenter.control.images import sync_image


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


# def list_files(ds, pattern):
#     search = vim.HostDatastoreBrowserSearchSpec()
#     search.matchPattern = pattern
#     n = '[' + ds.summary.name + ']'
#     search_ds = ds.browser.SearchDatastoreSubFolders_Task(n, search)
#     while search_ds.info.state != "success":
#         pass
#     results = search_ds.info.result
#     # print results
#     for rs in results:
#         # print rs
#         dsfolder = rs.folderPath
#         options = {}
#         for f in rs.file:
#             iso_name = f.path
#             path = dsfolder + iso_name
#             try:
#                 size = f.fileSize
#                 last_change_time = f.modification
#             except Exception as e:
#                 size = '0kb'
#                 last_change_time = '0kb'
#             options = {
#                 'iso_name': iso_name,
#                 'path': path,
#                 'size': size,
#                 'last_change_time': last_change_time,
#             }
#             yield options


def sync_datastore(platform, dc, si, content):
    obj = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)
    datastores = obj.view
    data_store_list = db.datastores.get_datastore_ds_name_by_platform_id(platform['id'], dc.name)
    print(data_store_list)

    for ds in datastores:
        ds_capacity = ds.summary.capacity
        ds_freespace = ds.summary.freeSpace
        ds_uncommitted = ds.summary.uncommitted if ds.summary.uncommitted else 0
        ds_provisioned = ds_capacity - ds_freespace + ds_uncommitted
        ds_overp = ds_provisioned - ds_capacity
        ds_overp_pct = (ds_overp * 100) / ds_capacity \
            if ds_capacity else 0
        # print dir(ds)
        ds_name = ds.name
        ds_mor_name = get_mor_name(ds)
        dc_name = dc.name
        dc_mor_name = get_mor_name(dc)
        type = ds.info.vmfs.type
        version = ds.info.vmfs.version
        uuid = ds.info.vmfs.uuid
        ssd = ds.info.vmfs.ssd
        local = ds.info.vmfs.local
        host = platform['ip']

        capacity = sizeof_fmt(ds_capacity)  # 存储容量
        free_capacity = sizeof_fmt(ds_freespace)  # 可用
        used_capacity = sizeof_fmt(ds_capacity - ds_freespace)

        if ds_name in data_store_list:
            data_store_list.remove(ds_name)
            db.datastores.update_datastore(platform['id'], ds_name, ds_mor_name, dc_name, dc_mor_name, capacity,
                                           used_capacity, free_capacity, type, version, uuid, ssd, local, host)
        else:
            db.datastores.create_datastore(platform['id'], ds_name, ds_mor_name, dc_name, dc_mor_name, capacity,
                                           used_capacity, free_capacity, type, version, uuid, ssd, local, host)

        sync_image(platform, ds)
    # print(11)
    if data_store_list:
        for ds_name in data_store_list:
            print(ds_name)
            db.datastores.delete_datastore_by_ds_name(ds_name)
    # print(22)


def get_datastore_by_platform_id(platform_id):
    datastores = db.datastores.get_datastore_by_platform_id(platform_id)
    datastore_list = []
    for datastore in datastores:
        ds_tmp = {
            'id': datastore.id,
            'platform_id': platform_id,
            'capacity': datastore.capacity,
            'used_capacity': datastore.used_capacity,
            'free_capacity': datastore.free_capacity,
            'type': datastore.type,
            'version': datastore.version,
            'uuid': datastore.uuid,
            'ssd': datastore.ssd,
            'local': datastore.local,
            'host': datastore.host,
            'ds_name': datastore.ds_name,
            'ds_mor_name': datastore.ds_mor_name,
            'dc_name': datastore.dc_name,
            'dc_mor_name': datastore.dc_mor_name,
        }
        datastore_list.append(ds_tmp)
    return datastore_list


def test_get_ds(platform_id):
    s, content, platform = get_connect(platform_id)

    # obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)

    datacenters_object_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datacenter], True)

    for dc in datacenters_object_view.view:
        obj = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)

        # manage.filesView
        # # 获取资源池
        # rp = get_largest_free_rp(s, dc)
        # return 'cccc'
        datastores = obj.view

        for ds in datastores:
            search = vim.HostDatastoreBrowserSearchSpec()
            search.matchPattern = '*.iso'
            n = '[' + ds.summary.name + ']'
            search_ds = ds.browser.SearchDatastoreSubFolders_Task(n, search)
            while search_ds.info.state != "success":
                pass
            results = search_ds.info.result
            for rs in search_ds.info.result:
                dsfolder = rs.folderPath
                for f in rs.file:
                    dsfile = f.path
                    print dsfolder + dsfile

        # for ds in datastores:
        #     # print(ds.host.summary.name)
        #
        #     ds_capacity = ds.summary.capacity
        #     ds_freespace = ds.summary.freeSpace
        #     ds_uncommitted = ds.summary.uncommitted if ds.summary.uncommitted else 0
        #     ds_provisioned = ds_capacity - ds_freespace + ds_uncommitted
        #     ds_overp = ds_provisioned - ds_capacity
        #     ds_overp_pct = (ds_overp * 100) / ds_capacity \
        #         if ds_capacity else 0
        #     print('dc:', dc.name, 'version:', ds.info.name)
        #     print('dc:', dc.name, 'capacity:', sizeof_fmt(ds_capacity))
        #     print('dc:', dc.name, 'freeSpace:', sizeof_fmt(ds_freespace))
        #     print('dc:', dc.name, 'ds_uncommitted :', sizeof_fmt(ds_uncommitted))
        #     print('dc:', dc.name, 'ds_provisioned ', sizeof_fmt(ds_provisioned))
        #
        #     # print('name:', ds.info.name)
        #     # print('type:', ds.info.type)
        #     # print('ssd:', ds.info.ssd)
        #     # print('ssd:', ds.info.ssd)
        #     # print('local:', ds.info.local)
        #     # print(dir(ds.summary.capacity))
