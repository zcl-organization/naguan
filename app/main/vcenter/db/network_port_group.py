# -*- coding:utf-8 -*-
from app.models import VCenterNetworkPortGroup
from app.exts import db


def network_create(name, mor_name, dc_name, dc_mor_name, platform_id):
    new_network = VCenterNetworkPortGroup()
    new_network.name = unicode(name)
    new_network.mor_name = mor_name
    new_network.dc_name = dc_name
    new_network.dc_mor_name = dc_mor_name
    new_network.platform_id = platform_id

    db.session.add(new_network)
    db.session.commit()


def network_list_by_mor_name(platform_id, mor_name):
    try:
        print(platform_id,mor_name)
        return db.session.query(VCenterNetworkPortGroup).filter_by(mor_name=mor_name).filter_by(platform_id=platform_id).first()
    except Exception as e:
        return False


def network_update(id, name, mor_name, dc_name, dc_mor_name):
    network_info = db.session.query(VCenterNetworkPortGroup).filter_by(id=id)
    network_info.name = name
    network_info.mor_name = mor_name
    network_info.dc_name = dc_name
    network_info.dc_mor_name = dc_mor_name

    db.session.commit()


def network_list_by_id(id):
    data = db.session.query(VCenterNetworkPortGroup).filter_by(id=id).first()
    return data


def list_all(platform_id):
    data = db.session.query(VCenterNetworkPortGroup).filter_by(platform_id=platform_id).all()
    return data