# -*- coding=utf-8 -*-
import json

from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_dvswitchs(platform_id, dvswitchs):
    """
    同步一组dvswitch数据
    """
    local_data = {
        (item.name, item.dc_name): item.id for item in db.dvswitch.dvswitch_all(platform_id)
    }
    
    for dvswitch in dvswitchs:
        parent = dvswitch.parent.parent
        sync_dvswitch(platform_id, dvswitch, parent)
        if (dvswitch.name, parent.name) in local_data.keys():
            local_data.pop((dvswitch.name, parent.name))
    
    for item in local_data.values():
        db.dvswitch.dvswitch_delete(item)


def sync_dvswitch(platform_id, dvswitch, parent):
    """
    单台dvswitch数据的收集
    """
    # host信息收集
    host_ids = []
    for item in dvswitch.config.host:
        host_ids.extend(
            db.host.get_host_id_by_uuid(item.config.host.summary.hardware.uuid)
        )

    data = dict(
        platform_id=platform_id,
        dc_name=parent.name,
        dc_mor_name=get_mor_name(parent),
        name=dvswitch.name,
        mor_name=get_mor_name(dvswitch),
        host_id=json.dumps(host_ids), 
        mtu=dvswitch.config.maxMtu,
        active_uplink_port=str(list(dvswitch.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.activeUplinkPort)),
        standby_uplink_port=str(list(dvswitch.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.standbyUplinkPort)),
        protocol=dvswitch.config.linkDiscoveryProtocolConfig.protocol,
        operation=dvswitch.config.linkDiscoveryProtocolConfig.operation,
        version=dvswitch.config.productInfo.version,
        describe=dvswitch.config.description,
        admin_name=dvswitch.config.contact.name,
        admin_describe=dvswitch.config.contact.contact,
        mulit_mode=dvswitch.config.multicastFilteringMode
    )

    dvswitch_info = db.dvswitch.find_dvswitch_by_name(platform_id, dvswitch.name, parent.name)
    if dvswitch_info:
        data['dvswitch_id'] = dvswitch_info.id
        db.dvswitch.dvswitch_update(**data)
    else:
        db.dvswitch.dvswitch_create(**data)
