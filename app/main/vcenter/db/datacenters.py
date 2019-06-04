# -*- coding=utf-8 -*-
from app.models import VCenterTree
from app.exts import db


# 获取datacenters
def get_datacenters(platform_id):
    return db.session.query(VCenterTree).filter_by(platform_id=platform_id).filter_by(type=2)


def sync_datacenters(platform_id, dc_name, dc_mor, dc_host_moc, dc_vm_moc, pid):
    data_center = db.session.query(VCenterTree).filter_by(platform_id=platform_id).\
        filter_by(type=2).filter_by(mor_name=dc_mor).first()
    if data_center:
        data_center.name = dc_name
        data_center.mor_name = dc_mor
        data_center.dc_host_folder_mor_name = dc_host_moc
        data_center.dc_mor_name = dc_mor
        data_center.dc_oc_name = dc_host_moc
        data_center.dc_vm_folder_mor_name = dc_vm_moc
        data_center.pid = pid
        db.session.add(data_center)
        db.session.commit()
        return dc_name
    else:
        new_data_center = VCenterTree()
        new_data_center.platform_id = platform_id
        new_data_center.type = 2
        new_data_center.name = dc_name
        new_data_center.mor_name = dc_mor
        new_data_center.dc_host_folder_mor_name = dc_host_moc
        new_data_center.dc_mor_name = dc_mor
        new_data_center.dc_oc_name = dc_host_moc
        new_data_center.dc_vm_folder_mor_name = dc_vm_moc
        new_data_center.pid = pid
        db.session.add(new_data_center)
        db.session.commit()


def del_datacenter(platform_id, dc_mor):
    data_center = db.session.query(VCenterTree).filter_by(platform_id=platform_id).\
        filter_by(type=2).filter_by(mor_name=dc_mor).first()
    db.session.delete(data_center)
    db.session.commit()
