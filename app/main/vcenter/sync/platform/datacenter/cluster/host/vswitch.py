# -*- coding=utf-8 -*-
import json
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_vswitchs(platform_id, vswitchs):
    """
    同步一组vswitch数据
    获取 -> 处理 -> 回收
    """
    local_data = {
        (item.name, item.host_mor_name): item.id for item in db.vswitch.get_vswitch_by_data(
            platform_id=platform_id
        )
    }

    for vswitch, host in vswitchs:
        sync_vswitch(platform_id, vswitch, host)
        check_vswitch = (vswitch.name, get_mor_name(host))
        if check_vswitch in local_data.keys():
            local_data.pop(check_vswitch)
        
    for item in local_data.values():
        db.vswitch.vswitch_delete(item)


def sync_vswitch(platform_id, vswitch, host):
    """
    同步单个vswitch数据
    """
    nics = [item for item in vswitch.spec.policy.nicTeaming.nicOrder.activeNic]
    data = dict(
        platform_id=platform_id,
        name=vswitch.name,
        mor_name="",     # TODO 获取mor_name的方式或是直接取消
        host_name=host.name,
        host_mor_name=get_mor_name(host),
        mtu=vswitch.mtu,
        num_of_port=vswitch.numPorts,
        nics=json.dumps(nics),
    )

    vswitch_info = db.vswitch.find_vswitch_by_name(platform_id, host.name, vswitch.name)
    if vswitch_info:
        data['vswitch_id'] = vswitch_info.id
        db.vswitch.vswitch_update(**data)
    else:
        db.vswitch.vswitch_create(**data)
