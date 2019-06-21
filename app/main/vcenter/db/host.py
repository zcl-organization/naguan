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
    new_host.ram = memory
    new_host.used_ram = used_memory
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
    return new_host.id


def get_host_by_name(name):
    return db.session.query(VCenterHost).filter_by(name=name).first()


def get_host_by_id(id):
    return db.session.query(VCenterHost).get(id)


def del_host(name):
    host = db.session.query(VCenterHost).filter_by(name=name).first()
    db.session.delete(host)
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
