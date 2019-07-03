# -*- coding: utf-8 -*-
from app.models import VCenterVswitch
from app.exts import db


def vswitch_create(platform_id, name, mor_name, host_name, host_mor_name, mtu, num_of_port, nics):
    """
    创建新的vswitch
    """
    new_vswitch = VCenterVswitch()
    new_vswitch.platform_id = platform_id
    new_vswitch.name = name
    new_vswitch.mor_name = mor_name
    new_vswitch.host_name = host_name
    new_vswitch.host_mor_name = host_mor_name
    new_vswitch.mtu = mtu
    new_vswitch.num_of_port = num_of_port
    new_vswitch.nics = nics

    db.session.add(new_vswitch)
    db.session.commit()


def vswitch_update(vswitch_id, platform_id, name, mor_name, host_name,
                    host_mor_name, mtu, num_of_port, nics):
    """
    更新指定id的vswitch
    """
    old_vswitch = db.session.query(VCenterVswitch).filter_by(id=vswitch_id).first()
    old_vswitch.platform_id = platform_id
    old_vswitch.name = name
    old_vswitch.mor_name = mor_name
    old_vswitch.host_name = host_name
    old_vswitch.host_mor_name = host_mor_name
    old_vswitch.mtu = mtu
    old_vswitch.num_of_port = num_of_port
    old_vswitch.nics = nics

    db.session.commit()


def vswitch_delete(vswitch_id):
    """
    删除指定id的Vswitch
    """
    old_vswitch = db.session.query(VCenterVswitch).filter_by(id=vswitch_id).first()
    if not old_vswitch:
        return

    db.session.delete(old_vswitch)
    db.session.commit()


def vswitch_all(platform_id):
    """
    列出所有的vswitch
    """
    return db.session.query(VCenterVswitch).filter_by(platform_id=platform_id).all()


def find_vswitch_by_id(vswitch_id):
    """
    通过vswitch_id查找数据
    """
    return db.session.query(VCenterVswitch).filter_by(id=vswitch_id).first()


def find_vswitch_by_name(platform_id, host_name, vswitch_name):
    """
    通过名称获取vswitch对象
    """
    return db.session.query(VCenterVswitch).filter_by(
        platform_id=platform_id,
        host_name=host_name,
        name=vswitch_name
    ).first()


def get_vswitch_by_data(platform_id=None, host_mor_name=None):
    """
    通过host数据来获取local数据  
    TODO
    """
    query = db.session.query(VCenterVswitch)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if host_mor_name:
        query = query.filter_by(host_mor_name=host_mor_name)
    return query.all()
