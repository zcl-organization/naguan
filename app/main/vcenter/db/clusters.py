# -*- coding=utf-8 -*-
from app.exts import db
from app.models import VCenterTree


def get_cluster_mor_name(platform_id, cluster_id):
    cluster = db.session.query(VCenterTree).get(cluster_id)
    if cluster.platform_id == int(platform_id) and cluster.type == 3:
        return cluster
    else:
        return None


def get_cluster_cluster_resource(platform_id, cluster_mor_name):
    return db.session.query(VCenterTree).filter_by(platform_id=platform_id).\
        filter_by(cluster_mor_name=cluster_mor_name).all()


# 查找dc下的cluster_name名称cluster
def get_cluster_by_name(platform_id, dc_id, cluster_name):
    return db.session.query(VCenterTree).filter_by(platform_id=platform_id).\
        filter_by(pid=dc_id).filter_by(name=cluster_name).first()

