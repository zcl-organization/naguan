# -*- coding=utf-8 -*-
from app.exts import db
from app.models import VCenterDatacenter
from sqlalchemy import exists


# 获取datacenters
def find_datacenters(platform_id=None, dc_id=None, dc_name=None):
    query = db.session.query(VCenterDatacenter)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if dc_id:
        query = query.filter_by(id=dc_id)
    if dc_name:
        query = query.filter_by(name=dc_name)
    return query


# 获取datacenters
def get_dc_by_id(id):
    return db.session.query(VCenterDatacenter).get(id)


# 判断是否存在datacenter名
def get_dc_by_name(dc_name):
    return db.session.query(VCenterDatacenter).filter_by(name=dc_name).first()


def del_datacenter(id):
    dc = db.session.query(VCenterDatacenter).get(id)
    db.session.delete(dc)
    db.session.commit()


def create_datacenter(name, mor_name, platform_id, host_nums, vm_nums, cluster_nums, network_nums,
                      datastore_nums, cpu_capacity, used_cpu, memory, used_memory, capacity, used_capacity):
    new_datacenter = VCenterDatacenter()
    new_datacenter.name = name
    new_datacenter.mor_name = mor_name
    new_datacenter.platform_id = platform_id
    new_datacenter.host_nums = host_nums
    new_datacenter.vm_nums = vm_nums
    new_datacenter.cluster_nums = cluster_nums
    new_datacenter.network_nums = network_nums
    new_datacenter.datastore_nums = datastore_nums
    new_datacenter.cpu_capacity = cpu_capacity
    new_datacenter.used_cpu = used_cpu
    new_datacenter.memory = memory
    new_datacenter.used_memory = used_memory
    new_datacenter.capacity = capacity
    new_datacenter.used_capacity = used_capacity
    db.session.add(new_datacenter)
    db.session.flush()
    db.session.commit()
    return new_datacenter


def update_datacenter(name, mor_name, platform_id, host_nums, vm_nums, cluster_nums, network_nums,
                      datastore_nums, cpu_capacity, used_cpu, memory, used_memory, capacity, used_capacity):
    datacenter_info = get_datacenter_by_mor_name(platform_id, mor_name)
    if name:
        datacenter_info.name = name
    datacenter_info.mor_name = mor_name
    datacenter_info.platform_id = platform_id
    if host_nums:
        datacenter_info.host_nums = host_nums
    if vm_nums:
        datacenter_info.vm_nums = vm_nums
    if cluster_nums:
        datacenter_info.cluster_nums = cluster_nums
    if network_nums:
        datacenter_info.network_nums = network_nums
    if datastore_nums:
        datacenter_info.datastore_nums = datastore_nums
    if cpu_capacity:
        datacenter_info.cpu_capacity = cpu_capacity
    if used_cpu:
        datacenter_info.used_cpu = used_cpu
    if memory:
        datacenter_info.memory = memory
    if used_memory:
        datacenter_info.used_memory = used_memory
    if capacity:
        datacenter_info.capacity = capacity
    if used_capacity:
        datacenter_info.used_capacity = used_capacity
    db.session.add(datacenter_info)
    db.session.flush()
    db.session.commit()
    return datacenter_info


# 判断dc是否在数据库中
def check_if_dc_exists_by_dc_name(dc_name):
    if_exists = db.session.query(
        exists().where(VCenterDatacenter.name == dc_name)
    ).scalar()
    return if_exists


def get_datacenter_by_mor_name(platform_id, mor_name):
    return db.session.query(VCenterDatacenter).filter_by(platform_id=platform_id).filter_by(mor_name=mor_name).first()


# 根据platform_id获取所有id
def get_datacenter_all_id(platform_id):
    return db.session.query(VCenterDatacenter.id).filter_by(platform_id=platform_id).all()


def get_datacenter_by_platform_id(platform_id):
    """
    通过platform_id获取数据
    """
    return db.session.query(VCenterDatacenter).filter_by(platform_id=platform_id).all()
