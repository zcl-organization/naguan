# -*- coding:utf-8 -*-
from app.models import VCenterSnapshot
from app.exts import db


def create_snapshot(name, mor_name, description, snapshot_id, state, snapshot_parent_id, create_time, vm_uuid, current):
    new_snapshot = VCenterSnapshot()
    new_snapshot.name = unicode(name)
    new_snapshot.mor_name = mor_name
    new_snapshot.description = unicode(description)
    new_snapshot.snapshot_id = snapshot_id
    new_snapshot.snapshot_parent_id = snapshot_parent_id
    new_snapshot.state = state
    new_snapshot.create_time = create_time
    new_snapshot.vm_uuid = vm_uuid
    new_snapshot.current = current

    db.session.add(new_snapshot)
    db.session.commit()


def update_snapshot(name, mor_name, description, snapshot_id, state, snapshot_parent_id, create_time, vm_uuid, current):
    snapshot_info = db.session.query(VCenterSnapshot).filter_by(vm_uuid=vm_uuid).filter_by(
        snapshot_id=snapshot_id).first()

    snapshot_info.name = unicode(name)
    snapshot_info.mor_name = mor_name
    snapshot_info.description = unicode(description)
    snapshot_info.state = state
    snapshot_info.snapshot_parent_id = snapshot_parent_id
    snapshot_info.create_time = create_time
    snapshot_info.current = current

    db.session.commit()


def get_all_snapshot_id_by_vm_uuid(vm_uuid):
    return db.session.query(VCenterSnapshot.snapshot_id).filter_by(vm_uuid=vm_uuid).all()


def delete_snapshot_by_snapshot_id(vm_uuid, snapshot_id):
    db.session.query(VCenterSnapshot).filter_by(vm_uuid=vm_uuid).filter_by(snapshot_id=snapshot_id).delete(
        synchronize_session=False)


def delete_snapshot_by_vm_uuid(vm_uuid):
    db.session.query(VCenterSnapshot).filter_by(vm_uuid=vm_uuid).delete(synchronize_session=False)


def get_snapshot_by_snapshot_id(vm_uuid, snapshot_id):
    return db.session.query(VCenterSnapshot).filter_by(vm_uuid=vm_uuid).filter_by(snapshot_id=snapshot_id).first()


def get_snapshot_list(platform_id, snapshot_id, vm_uuid):
    query = db.session.query(VCenterSnapshot)
    # if platform_id:
    #     query = query.filter_by(platform_id=platform_id)
    if snapshot_id:
        query = query.filter_by(snapshot_id=snapshot_id)
    if vm_uuid:
        query = query.filter_by(vm_uuid=vm_uuid)
    data = query.all()
    return data
