# -*- coding:utf-8 -*-
import time

from flask_restful.representations import json
from pyVim import connect
import atexit

from pyVmomi import vmodl
from pyVmomi import vim

from app.main.vcenter.control.utils import get_connect, get_mor_name

from app.main.vcenter import db
from app.main.vcenter.control.images import sync_image
from app.exts import celery


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


@celery.task()
def sync_datastore(platform, dc, si, content=None):
    print ('sync_dc_start:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))
    # content = si.RetrieveContent()
    obj = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)
    datastores = obj.view
    data_store_list = db.datastores.get_datastore_ds_name_by_platform_id(platform['id'], dc.name)
    # print(data_store_list)

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
        # local = ds.info.vmfs.local
        if ds.info.vmfs.local:
            local = True
        else:
            local = False

        # host = platform['ip']
        host = ds.host[0].key.name
        capacity = ds_capacity  # 存储容量
        free_capacity = ds_freespace  # 可用
        used_capacity = ds_capacity - ds_freespace

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
            # print(ds_name)
            db.datastores.delete_datastore_by_ds_name(ds_name)
    print ('sync_dc_stop:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))


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
