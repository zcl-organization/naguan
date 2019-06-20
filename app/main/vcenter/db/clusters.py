# -*- coding=utf-8 -*-
from app.exts import db
from app.models import VCenterTree
from app.models import VCenterClusters


def get_cluster_mor_name(platform_id, cluster_id):
    cluster = db.session.query(VCenterTree).get(cluster_id)
    if cluster.platform_id == int(platform_id) and cluster.type == 3:
        return cluster
    else:
        return None


# 查找dc下的cluster_name名称的cluster
def get_cluster_by_name(platform_id, dc_name, cluster_name):
    return db.session.query(VCenterClusters).filter_by(platform_id=platform_id).\
        filter_by(dc_name=dc_name).filter_by(name=cluster_name).first()


def get_cluster_cluster_resource(platform_id, cluster_mor_name):
    return db.session.query(VCenterTree).filter_by(platform_id=platform_id).\
        filter_by(cluster_mor_name=cluster_mor_name).all()


def get_clusters(platform_id):
    return db.session.query(VCenterTree).filter_by(platform_id=platform_id).all()


def create_cluster(name, mor_name, platform_id, dc_name, dc_mor_name, cpu_nums, cpu_capacity,
                   used_cpu, memory, used_memory, capacity, used_capacity, host_nums, vm_nums):
    new_cluster = VCenterClusters()
    new_cluster.name = name
    new_cluster.mor_name = mor_name
    new_cluster.platform_id = platform_id
    new_cluster.dc_name = dc_name
    new_cluster.dc_mor_name = dc_mor_name
    new_cluster.cpu_nums = cpu_nums
    new_cluster.cpu_capacity = cpu_capacity
    new_cluster.used_cpu = used_cpu
    new_cluster.memory = memory
    new_cluster.used_memory = used_memory
    new_cluster.capacity = capacity
    new_cluster.used_capacity = used_capacity
    new_cluster.host_nums = host_nums
    new_cluster.vm_nums = vm_nums
    db.session.add(new_cluster)
    db.session.flush()
    db.session.commit()
    return new_cluster.id
