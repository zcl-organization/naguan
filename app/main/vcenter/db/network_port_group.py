# -*- coding:utf-8 -*-
from app.models import VCenterNetworkPortGroup
from app.exts import db


def network_create(name, mor_name, dc_name, dc_mor_name, platform_id, host):
    """
    vswitch 数据库存储
    """
    new_network = VCenterNetworkPortGroup()
    new_network.name = unicode(name)
    new_network.mor_name = mor_name
    new_network.dc_name = dc_name
    new_network.dc_mor_name = dc_mor_name
    new_network.platform_id = platform_id
    new_network.host = host

    db.session.add(new_network)
    db.session.commit()


def network_list_by_mor_name(platform_id, mor_name):
    try:
        # print(platform_id,mor_name)
        return db.session.query(VCenterNetworkPortGroup).filter_by(mor_name=mor_name).filter_by(platform_id=platform_id).first()
    except Exception as e:
        return False


def network_update(id, name, mor_name, dc_name, dc_mor_name):
    """
    vswitch 数据库更新
    """
    network_info = db.session.query(VCenterNetworkPortGroup).filter_by(id=id).first()
    network_info.name = name
    network_info.mor_name = mor_name
    network_info.dc_name = dc_name
    network_info.dc_mor_name = dc_mor_name

    db.session.commit()


def network_delete(id):
    """
    vswitch 数据库删除
    """
    del_portgroup = db.session.query(VCenterNetworkPortGroup).filter_by(id=id).first()
    db.session.delete(del_portgroup)
    db.session.commit()


def network_list_by_id(id):
    return db.session.query(VCenterNetworkPortGroup).filter_by(id=id).first()


def list_all(platform_id):
    return db.session.query(VCenterNetworkPortGroup).filter_by(platform_id=platform_id).all()


def find_portgroup_by_name(portgroup_name, host_name):
    """
    查找端口组通过端口组名称和host名称
    """
    return db.session.query(VCenterNetworkPortGroup).filter_by(host=host_name, name=portgroup_name).first()

def find_portgroup_by_id(portgroup_id):
    """
    通过端口组id查询相关数据
    """
    return network_list_by_id(portgroup_id)

