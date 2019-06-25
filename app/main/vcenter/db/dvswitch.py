# -*- coding: utf-8 -*-
from app.models import VCenterDvswitch
from app.exts import db


def dvswitch_create(platform_id, dc_name, dc_mor_name, name, mor_name, host_id, mtu, active_uplink_port, standby_uplink_port, 
        protocol, operation, version, describe, admin_name, admin_describe, mulit_mode):
    """
    创建新的dvswitch
    """
    new_dvswitch = VCenterDvswitch()
    new_dvswitch.platform_id = platform_id
    new_dvswitch.dc_name = dc_name
    new_dvswitch.dc_mor_name = dc_mor_name
    new_dvswitch.name = name
    new_dvswitch.mor_name = mor_name
    new_dvswitch.host_id = host_id
    new_dvswitch.mtu = mtu
    new_dvswitch.active_uplink_port = active_uplink_port
    new_dvswitch.standby_uplink_port = standby_uplink_port
    new_dvswitch.protocol = protocol
    new_dvswitch.operation = operation
    new_dvswitch.version = version
    new_dvswitch.describe = describe
    new_dvswitch.admin_name = admin_name
    new_dvswitch.admin_describe = admin_describe
    new_dvswitch.mulit_mode = mulit_mode

    db.session.add(new_dvswitch)
    db.session.commit()


def dvswitch_update(dvswitch_id, dc_name, dc_mor_name, platform_id, name, mor_name, host_id, mtu, 
        active_uplink_port, standby_uplink_port, protocol, operation, version,
        describe, admin_name, admin_describe, mulit_mode):
    """
    更新指定id的dvswitch
    """
    old_dvswitch = db.session.query(VCenterDvswitch).filter_by(id=dvswitch_id).first()
    
    old_dvswitch.platform_id = platform_id
    old_dvswitch.dc_name = dc_name
    old_dvswitch.dc_mor_name = dc_mor_name
    old_dvswitch.name = name
    old_dvswitch.mor_name = mor_name
    old_dvswitch.host_id = host_id
    old_dvswitch.mtu = mtu
    old_dvswitch.active_uplink_port = active_uplink_port
    old_dvswitch.standby_uplink_port = standby_uplink_port
    old_dvswitch.protocol = protocol
    old_dvswitch.operation = operation
    old_dvswitch.version = version
    old_dvswitch.describe = describe
    old_dvswitch.admin_name = admin_name
    old_dvswitch.admin_describe = admin_describe
    old_dvswitch.mulit_mode = mulit_mode

    db.session.commit()


def dvswitch_delete(dvswitch_id):
    """
    删除指定id的dvswitch
    """
    old_vswitch = db.session.query(VCenterDvswitch).filter_by(id=dvswitch_id).first()
    if not old_vswitch:
        return

    db.session.delete(old_vswitch)
    db.session.commit()


def dvswitch_all(platform_id):
    """
    列出所有的dvswitch
    """
    return db.session.query(VCenterDvswitch).filter_by(platform_id=platform_id).all()


def find_dvswitch_by_id(dvswitch_id):
    """
    通过dvswitch_id查找数据
    """
    return db.session.query(VCenterDvswitch).filter_by(id=dvswitch_id).first()


def find_dvswitch_by_name(platform_id, dvswitch_name, dc_name):
    """
    通过名称获取dvswitch对象   (待处理)
    """
    return db.session.query(VCenterDvswitch).filter_by(
        platform_id=platform_id,
        name=dvswitch_name,
        dc_name=dc_name
    ).first()
