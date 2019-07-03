# -*- coding=utf-8 -*-
from app.exts import db
from app.models import VCenterHost


def add_host(name, mor_mame, dc_name, dc_mor_name, cluster_name, cluster_mor_name, port, power_state, connection_state,
             maintenance_mode, platform_id, uuid, cpu_cores, used_cpu, memory, used_memory, capacity, used_capacity,
             cpu_mhz, cpu_model, version, image, build, full_name, boot_time, uptime, vm_nums, network_nums):
    new_host = VCenterHost()
    new_host.name = name
    new_host.mor_name = mor_mame
    new_host.dc_name = dc_name
    new_host.dc_mor_name = dc_mor_name
    new_host.cluster_name = cluster_name
    new_host.cluster_mor_name = cluster_mor_name
    new_host.port = port
    new_host.power_state = power_state
    new_host.connection_state = connection_state
    new_host.maintenance_mode = maintenance_mode
    new_host.platform_id = platform_id
    new_host.uuid = uuid
    new_host.cpu_cores = cpu_cores
    new_host.used_cpu = used_cpu
    new_host.memory = memory
    new_host.used_memory = used_memory
    new_host.capacity = capacity
    new_host.used_capacity = used_capacity
    new_host.cpu_mhz = cpu_mhz
    new_host.cpu_model = cpu_model
    new_host.version = version
    new_host.image = image
    new_host.build = build
    new_host.full_name = full_name
    new_host.boot_time = boot_time
    new_host.uptime = uptime
    new_host.vm_nums = vm_nums
    new_host.network_nums = network_nums
    db.session.add(new_host)
    db.session.flush()
    db.session.commit()
    return new_host


def update_host(name, mor_mame, dc_name, dc_mor_name, cluster_name, cluster_mor_name, port, power_state,
                connection_state, maintenance_mode, platform_id, uuid, cpu_cores, used_cpu, memory,
                used_memory, capacity, used_capacity, cpu_mhz, cpu_model, version, image, build,
                full_name, boot_time, uptime, vm_nums, network_nums):
    cluster_info = get_host_by_name(platform_id, name)
    cluster_info.name = name
    cluster_info.mor_name = mor_mame
    cluster_info.dc_name = dc_name
    cluster_info.dc_mor_name = dc_mor_name
    cluster_info.cluster_name = cluster_name
    cluster_info.cluster_mor_name = cluster_mor_name
    cluster_info.port = port
    cluster_info.power_state = power_state
    cluster_info.connection_state = connection_state
    cluster_info.maintenance_mode = maintenance_mode
    cluster_info.platform_id = platform_id
    cluster_info.uuid = uuid
    cluster_info.cpu_cores = cpu_cores
    cluster_info.used_cpu = used_cpu
    cluster_info.memory = memory
    cluster_info.used_memory = used_memory
    cluster_info.capacity = capacity
    cluster_info.used_capacity = used_capacity
    cluster_info.cpu_mhz = cpu_mhz
    cluster_info.cpu_model = cpu_model
    cluster_info.version = version
    cluster_info.image = image
    cluster_info.build = build
    cluster_info.full_name = full_name
    cluster_info.boot_time = boot_time
    cluster_info.uptime = uptime
    cluster_info.vm_nums = vm_nums
    cluster_info.network_nums = network_nums
    db.session.add(cluster_info)
    db.session.flush()
    db.session.commit()
    return cluster_info


def get_host_by_name(platform_id, name):
    return db.session.query(VCenterHost).filter_by(platform_id=platform_id).filter_by(name=name).first()


def get_host_by_id(id):
    return db.session.query(VCenterHost).get(id)


def del_host_by_id(id):
    db.session.query(VCenterHost).filter_by(id=id).delete(synchronize_session=False)
    db.session.commit()


def find_host(platform_id=None, id=None, host_name=None, dc_name=None, cluster_name=None):
    # return db.session.query(VCenterHost).filter_by(platform_id=platform_id).all()
    query = db.session.query(VCenterHost)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if id:
        query = query.filter_by(id=id)
    if host_name:
        query = query.filter_by(name=host_name)
    if dc_name:
        query = query.filter_by(dc_name=dc_name)
    if cluster_name:
        query = query.filter_by(cluster_name=cluster_name)

    return query


def put_host_maintenance_mode(host_id, maintenance_mode):
    host = db.session.query(VCenterHost).get(host_id)
    host.maintenance_mode = maintenance_mode
    db.session.commit()


# 根据platform_id获取所有id
def get_host_all_id(platform_id):
    return db.session.query(VCenterHost.id).filter_by(platform_id=platform_id).all()


def get_host_id_by_uuid(uuid):
    """
    通过host的uuid获取对应表id  用户dvs的host信息收集
    """
    return db.session.query(VCenterHost.id).filter_by(uuid=uuid).first()


def get_host_by_data(platform_id=None, dc_mor_name=None, cluster_mor_name=None):
    """
    通过host数据来获取local数据  
    TODO
    """
    query = db.session.query(VCenterHost)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if dc_mor_name:
        query = query.filter_by(dc_mor_name=dc_mor_name)
    if cluster_mor_name:
        query = query.filter_by(cluster_mor_name=cluster_mor_name)
    return query.all()


def get_host_by_mor_name(platform_id, mor_name):
    return db.session.query(VCenterHost).filter_by(
        platform_id=platform_id, mor_name=mor_name
    ).first()
