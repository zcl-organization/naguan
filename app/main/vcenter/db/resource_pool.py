from app.exts import db
from app.models import VCenterResourcePool


def create_resource_pool(platform_id, dc_name, dc_mor_name, cluster_name, cluster_mor_name, name, mor_name, parent_name,
                         over_all_status, cpu_expand_able_reservation,
                         cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage, cpu_max_usage,
                         memory_expand_able_reservation, memory_reservation, memory_limit, memory_shares, memory_level,
                         memory_over_all_usage, memory_max_usage):
    new_rp = VCenterResourcePool()
    new_rp.platform_id = platform_id
    new_rp.dc_name = dc_name
    new_rp.dc_mor_name = dc_mor_name
    new_rp.cluster_name = cluster_name
    new_rp.cluster_mor_name = cluster_mor_name
    new_rp.name = name
    new_rp.mor_name = mor_name
    new_rp.parent_name = parent_name
    new_rp.over_all_status = over_all_status
    new_rp.cpu_expand_able_reservation = cpu_expand_able_reservation
    new_rp.cpu_reservation = cpu_reservation
    new_rp.cpu_limit = cpu_limit
    new_rp.cpu_shares = cpu_shares
    new_rp.cpu_level = cpu_level
    new_rp.cpu_over_all_usage = cpu_over_all_usage
    new_rp.cpu_max_usage = cpu_max_usage
    new_rp.memory_expand_able_reservation = memory_expand_able_reservation
    new_rp.memory_reservation = memory_reservation
    new_rp.memory_limit = memory_limit
    new_rp.memory_shares = memory_shares
    new_rp.memory_level = memory_level
    new_rp.memory_over_all_usage = memory_over_all_usage
    new_rp.memory_max_usage = memory_max_usage
    db.session.add(new_rp)
    db.session.commit()


def update_resource_pool(rp_id, platform_id, dc_name, dc_mor_name, cluster_name, cluster_mor_name, name, mor_name,
                         parent_name, over_all_status, cpu_expand_able_reservation,
                         cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage, cpu_max_usage,
                         memory_expand_able_reservation, memory_reservation, memory_limit, memory_shares, memory_level,
                         memory_over_all_usage, memory_max_usage):
    rp_info = db.session.query(VCenterResourcePool).filter_by(id=rp_id).filter_by(platform_id=platform_id).first()

    rp_info.dc_name = dc_name
    rp_info.dc_mor_name = dc_mor_name
    rp_info.name = name
    rp_info.mor_name = mor_name
    rp_info.cluster_name = cluster_name
    rp_info.cluster_mor_name = cluster_mor_name
    rp_info.parent_name = parent_name
    rp_info.over_all_status = over_all_status
    rp_info.cpu_expand_able_reservation = cpu_expand_able_reservation
    rp_info.cpu_reservation = cpu_reservation
    rp_info.cpu_limit = cpu_limit
    rp_info.cpu_shares = cpu_shares
    rp_info.cpu_level = cpu_level
    rp_info.cpu_over_all_usage = cpu_over_all_usage
    rp_info.cpu_max_usage = cpu_max_usage
    rp_info.memory_expand_able_reservation = memory_expand_able_reservation
    rp_info.memory_reservation = memory_reservation
    rp_info.memory_limit = memory_limit
    rp_info.memory_shares = memory_shares
    rp_info.memory_level = memory_level
    rp_info.memory_over_all_usage = memory_over_all_usage
    rp_info.memory_max_usage = memory_max_usage

    db.session.commit()


def get_rp_by_mor_name(platform_id, mor_name):
    return db.session.query(VCenterResourcePool).filter_by(platform_id=platform_id).filter_by(mor_name=mor_name).first()


def get_resource_pool_list(platform_id, dc_mor_name, cluster_mor_name):
    query = db.session.query(VCenterResourcePool)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if dc_mor_name:
        query = query.filter_by(dc_mor_name=dc_mor_name)
    if cluster_mor_name:
        query = query.filter_by(cluster_mor_name=cluster_mor_name)
    return query.all()
