# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name


def sync_network_portgroup(platform_id, portgroups):
    """
    同步所有端口组
    获取 -> 处理 -> 回收
    """
    local_vs_portgroup = {
        (item.name, item.host): item.id for item in db.network_port_group.list_all(platform_id)
    }
    local_dvs_portgroup = {
        (item.name, item.switch): item.id for item in db.network_dvs_port_group.dvs_portgroup_all(platform_id)
    }
    
    for portgroup in portgroups:
        datacenter = portgroup.parent.parent  # portgroup.folder.datacenter
        if isinstance(portgroup, vim.dvs.DistributedVirtualPortgroup):
            switch = portgroup.config.distributedVirtualSwitch
            sync_dvs_portgroup(platform_id, portgroup, switch, datacenter)
            if (portgroup.name, switch.name) in local_dvs_portgroup.keys():
                local_dvs_portgroup.pop((portgroup.name, switch.name))
        else:
            if not portgroup.host:
                sync_vs_portgroup(platform_id, portgroup, None, datacenter)
                if (portgroup.name, None) in local_vs_portgroup.keys():
                    local_vs_portgroup.pop((portgroup.name, host.name))
            else:
                for host in portgroup.host:
                    sync_vs_portgroup(platform_id, portgroup, host, datacenter)
                    if (portgroup.name, host.name) in local_vs_portgroup.keys():
                        local_vs_portgroup.pop((portgroup.name, host.name))

    for item in local_vs_portgroup.values():
        db.network_port_group.network_delete(item)
    for item in local_dvs_portgroup.values():
        db.network_dvs_port_group.dvs_network_delete(item)


def sync_vs_portgroup(platform_id, vs_portgroup, host, datacenter):
    """
    同步单个vswitch端口组
    """
    host_name = host.name if host else None
    network_info = db.network_port_group.find_portgroup_by_name(vs_portgroup.name, host_name)
    if not network_info:
        db.network_port_group.network_create(
            name=vs_portgroup.name,
            mor_name=get_mor_name(vs_portgroup),
            dc_name=datacenter.name,
            dc_mor_name=get_mor_name(datacenter),
            platform_id=platform_id,
            host=host_name
        )
    else:
        db.network_port_group.network_update(
            id=network_info.id,
            name=vs_portgroup.name,
            mor_name=get_mor_name(vs_portgroup),
            dc_name=datacenter.name,
            dc_mor_name=get_mor_name(datacenter)
        )


def sync_dvs_portgroup(platform_id, dvs_portgroup, switch, parent):
    """
    同步单个Dswitch端口组
    """
    network_info = db.network_dvs_port_group.find_dvs_portgroup_by_name(dvs_portgroup.name, switch.name)
    if not network_info:
        db.network_dvs_port_group.dvs_network_create(
            name=dvs_portgroup.name,
            mor_name=get_mor_name(dvs_portgroup),
            dc_name=parent.name,
            dc_mor_name=get_mor_name(parent),
            platform_id=platform_id,
            switch=switch.name,
            uplink=dvs_portgroup.config.uplink
        )
    else:
        db.network_dvs_port_group.dvs_network_update(
            id=network_info.id,
            name=dvs_portgroup.name,
            mor_name=get_mor_name(dvs_portgroup),
            dc_name=parent.name,
            dc_mor_name=get_mor_name(parent)
        )
