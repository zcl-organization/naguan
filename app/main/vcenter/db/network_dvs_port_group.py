# -*- coding:utf-8 -*-
from app.models import VCenterNetworkDistributedSwitchPortGroup
from app.exts import db


def dvs_network_create(name, mor_name, dc_name, dc_mor_name, platform_id, switch, uplink=False):
    """
    dvswitch 数据库存储
    """
    new_network = VCenterNetworkDistributedSwitchPortGroup()
    new_network.name = unicode(name)
    new_network.mor_name = mor_name
    new_network.dc_name = dc_name
    new_network.dc_mor_name = dc_mor_name
    new_network.platform_id = platform_id
    new_network.switch = switch
    new_network.uplink = uplink

    db.session.add(new_network)
    db.session.commit()


def dvs_network_update(id, name, mor_name, dc_name, dc_mor_name):
    """
    dvswitch 数据库更新
    TODO  switch 信息是否不需要更新
    """
    network_info = db.session.query(VCenterNetworkDistributedSwitchPortGroup).filter_by(id=id)
    network_info.name = name
    network_info.mor_name = mor_name
    network_info.dc_name = dc_name
    network_info.dc_mor_name = dc_mor_name

    db.session.commit()


def dvs_network_delete(id):
    """
    dvswitch 数据库删除
    """
    del_portgroup = db.session.query(VCenterNetworkDistributedSwitchPortGroup).filter_by(id=id).first()
    db.session.delete(del_portgroup)
    db.session.commit()


def find_dvs_portgroup_by_name(portgroup_name, switch_name):
    """
    查找端口组通过端口组名称和host名称
    """
    return db.session.query(VCenterNetworkDistributedSwitchPortGroup).filter_by(switch=switch_name, name=portgroup_name).first()


def find_dvs_portgroup_by_id(portgroup_id):
    """
    通过端口组id查询相关数据
    """
    return db.session.query(VCenterNetworkDistributedSwitchPortGroup).filter_by(id=portgroup_id).first()


def dvs_portgroup_all(platform_id):
    """
    列出platform_id表示机子下属的所有端口组
    """
    return db.session.query(VCenterNetworkDistributedSwitchPortGroup).filter_by(platform_id=platform_id).all()


