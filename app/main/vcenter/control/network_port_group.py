# -*- coding:utf-8 -*-
from pyVmomi import vim

from app.main.vcenter.control.utils import get_obj, get_mor_name
# from app.main.vcenter.control.vcenter import get_connect
from app.main.vcenter import db


def sync_network_port_group(netwroks, dc_name, dc_mor_name, platform_id):
    if netwroks:
        for network in netwroks:
            # pass
            # 判断是否存在网络
            network_mor_name = get_mor_name(network)
            # network_info = db_network.network_list_by_mor_name(platform_id, network_mor_name)
            network_info = db.network_port_group.network_list_by_mor_name(platform_id, network_mor_name)
            if not network_info:
                # db_network.network_create(network.name, network_mor_name, dc_name, dc_mor_name, platform_id)
                db.network_port_group.network_create(network.name, network_mor_name, dc_name, dc_mor_name, platform_id)
            else:
                # print(network_info)
                # db_network.network_update(network_info.get('id'), network.name, network_mor_name, dc_name, dc_mor_name)
                db.network_port_group.network_update(network_info.id, network.name, network_mor_name, dc_name,
                                                     dc_mor_name)


def get_network_by_id(id):
    return db.network_port_group.network_list_by_id(id)


def get_network_port_group_all(platform_id):
    port_groups = db.network_port_group.list_all(platform_id)

    network_port_group_list = []

    for group in port_groups:
        group_tmp = dict()
        group_tmp['id'] = group.id
        group_tmp['name'] = group.name
        group_tmp['mor_name'] = group.mor_name
        group_tmp['dc_name'] = group.dc_name
        group_tmp['dc_mor_name'] = group.dc_mor_name
        group_tmp['platform_id'] = group.platform_id

        network_port_group_list.append(group_tmp)
    return network_port_group_list
