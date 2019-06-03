# -*- coding=utf-8 -*-
from app.models import VCenterTree
from app.exts import db


# 获取datacenters
def get_datacenters(platform_id):
    return db.session.query(VCenterTree).filter_by(platform_id=platform_id).filter_by(type=2)


def sync_datacenters(platform_id, dc_name, dc_mor, dc_host_moc, dc_vm_moc):
    data_center = db.session.query(VCenterTree).filter_by(platform_id=platform_id).\
        filter_by(type=2).filter_by(name=dc_name).first()
    if data_center:
        pass
    else:
        pass


