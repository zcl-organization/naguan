# -*- coding=utf-8 -*-
import json
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name

from app.main.vcenter.control.images import sync_image


def sync_datastores(platform_id, datastores):
    """
    同步一组datastore数据
    获取 -> 处理 -> 回收
    """
    local_data = {
        item.uuid: item.id for item in db.datastores.get_datastore_by_platform_id(platform_id)
    }
    
    for datastore in datastores:
        parent = datastore.parent.parent  # datastore.folder.datacenter
        sync_datastore(platform_id, datastore, parent)
        sync_images(platform_id, datastore)
        if datastore.info.vmfs.uuid in local_data.keys():
            local_data.pop(datastore.info.vmfs.uuid)
    
    for item in local_data.values():
        db.datastores.delete_datastore_by_id(item)


def sync_datastore(platform_id, datastore, parent):
    """
    同步单个datastore数据
    """
    host_names = []
    for host in datastore.host:
        host_names.append(host.key.name)

    data = dict(
        platform_id=platform_id,
        ds_name=datastore.name,
        ds_mor_name=get_mor_name(datastore),
        dc_name=parent.name,
        dc_mor_name=get_mor_name(parent),
        capacity=datastore.summary.capacity,
        used_capacity=datastore.summary.capacity-datastore.summary.freeSpace, 
        free_capacity=datastore.summary.freeSpace,
        type=datastore.info.vmfs.type,
        version=datastore.info.vmfs.version,
        uuid=datastore.info.vmfs.uuid,
        ssd=datastore.info.vmfs.ssd,
        local=True if datastore.info.vmfs.local else False,
        host=json.dumps(host_names)
    )

    datastore_info = db.datastores.find_datastore_by_uuid(datastore.info.vmfs.uuid)
    if datastore_info:
        db.datastores.update_datastore(**data)
    else:
        db.datastores.create_datastore(**data)


def sync_images(platform_id, datastore):
    """
    同步DS下的所有镜像文件,直接调用原有函数
    TODO
    """
    platform = {
        "id": platform_id
    }
    sync_image(platform, datastore)
