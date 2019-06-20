# -*- coding=utf-8 -*-
from app.models import VCenterTree
from app.exts import db
from app.models import VCenterDatacenter


# 获取datacenters
def get_datacenters(platform_id):
    return db.session.query(VCenterDatacenter).filter_by(platform_id=platform_id).all()


# 获取datacenters
def get_dc_by_id(id):
    return db.session.query(VCenterDatacenter).get(id)


# 判断是否存在datacenter名
def get_dc_name(dc_name):
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
    return new_datacenter.id



