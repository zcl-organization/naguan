# -*- coding:utf-8 -*-

# from pyVmomi import vim
from app.main.vcenter.control.utils import get_mor_name
from app.main.vcenter import db
from app.exts import celery


def sync_snap_info(platform_id, snapshotlist, vm, parent_id=None, depth=1):
    snapshot_id_list = []
    current_snapshot = vm.snapshot.currentSnapshot
    # print(current_snapshot)
    current_snapshot_mor_name = get_mor_name(current_snapshot)
    if current_snapshot_mor_name == get_mor_name(snapshotlist.snapshot):
        current_snapshot_status = True
    else:
        current_snapshot_status = False

    create_time = snapshotlist.createTime.strftime("%Y-%m-%d %H:%M:%S")

    # 远端存在的 snapshot_id
    snapshot_id_list.append(snapshotlist.id)

    # 判断本地是否已存在snapshot_id
    snapshot = db.snapshots.get_snapshot_by_snapshot_id(vm.summary.config.uuid, snapshotlist.id)

    if snapshot:
        db.snapshots.update_snapshot(name=snapshotlist.name, mor_name=get_mor_name(snapshotlist.snapshot),
                                     description=snapshotlist.description, state=snapshotlist.state,
                                     snapshot_id=snapshotlist.id, snapshot_parent_id=parent_id,
                                     create_time=create_time, vm_uuid=vm.summary.config.uuid,
                                     current=current_snapshot_status)
    else:
        db.snapshots.create_snapshot(name=snapshotlist.name, mor_name=get_mor_name(snapshotlist.snapshot),
                                     description=snapshotlist.description, state=snapshotlist.state,
                                     snapshot_id=snapshotlist.id, snapshot_parent_id=parent_id,
                                     create_time=create_time, vm_uuid=vm.summary.config.uuid,
                                     current=current_snapshot_status)

    maxdepth = 10
    if depth < maxdepth:
        if len(snapshotlist.childSnapshotList) > 0:
            for snapshot in snapshotlist.childSnapshotList:

                if hasattr(snapshot, "childSnapshotList"):
                    snapshot_id = sync_snap_info(platform_id, snapshot, vm, snapshotlist.id, depth + 1)
                    snapshot_id_list = snapshot_id_list + snapshot_id
    return snapshot_id_list


#
# @celery.task()
# def sync_snapshot(platform_id, vm_uuid):
#     local_vm = db.instances.list_by_uuid(platform_id, vm_uuid)
#     si, content, platform = get_connect(platform_id)
#     vm = get_obj(content, [vim.VirtualMachine], local_vm.vm_name)
#
#     if vm.snapshot is not None:
#
#         # 根据云主机id获取所有快照
#         snapshot_list = []
#         snapshots_id_list_db = db.snapshots.get_all_snapshot_id_by_vm_uuid(vm.summary.config.uuid)
#         for snapshots in snapshots_id_list_db:
#             snapshot_list.append(snapshots.snapshot_id)
#
#         # 同步所有快照并返回远端vcenter中的快照id
#         snapshot_id_list = []
#         for snapshot in vm.snapshot.rootSnapshotList:
#             snapshot_id = sync_snap_info(platform_id, snapshot, vm)
#             snapshot_id_list = snapshot_id_list + snapshot_id
#
#         # print(snapshot_id_list)
#         # 删除本地多出来的快照
#         for snapshot_id in snapshot_id_list:
#             if snapshot_id in snapshot_list:
#                 snapshot_list.remove(snapshot_id)
#
#         if snapshot_list:
#             for snapshot_id in snapshot_list:
#                 db.snapshots.delete_snapshot_by_snapshot_id(vm.summary.config.uuid, snapshot_id)
#
#     else:
#         # 删除 vm_uuid 相关的snapshot
#         db.snapshots.delete_snapshot_by_vm_uuid(vm.summary.config.uuid)


@celery.task()
def sync_snapshot(platform_id, vm):
    if vm.snapshot is not None:

        # 根据云主机id获取所有快照
        snapshot_list = []
        snapshots_id_list_db = db.snapshots.get_all_snapshot_id_by_vm_uuid(vm.summary.config.uuid)
        for snapshots in snapshots_id_list_db:
            snapshot_list.append(snapshots.snapshot_id)

        # 同步所有快照并返回远端vcenter中的快照id
        snapshot_id_list = []
        for snapshot in vm.snapshot.rootSnapshotList:
            snapshot_id = sync_snap_info(platform_id, snapshot, vm)
            snapshot_id_list = snapshot_id_list + snapshot_id

        # print(snapshot_id_list)
        # 删除本地多出来的快照
        for snapshot_id in snapshot_id_list:
            if snapshot_id in snapshot_list:
                snapshot_list.remove(snapshot_id)

        if snapshot_list:
            for snapshot_id in snapshot_list:
                db.snapshots.delete_snapshot_by_snapshot_id(vm.summary.config.uuid, snapshot_id)

    else:
        # 删除 vm_uuid 相关的snapshot
        db.snapshots.delete_snapshot_by_vm_uuid(vm.summary.config.uuid)


def get_snapshot_by_snapshot_id(vm, snapshot_id):
    return db.snapshots.get_snapshot_by_snapshot_id(vm.summary.config.uuid, snapshot_id)


def get_snapshot_list(platform_id, snapshot_id, vm_uuid, pgnum):
    results, pg = db.snapshots.get_snapshot_list(platform_id, snapshot_id, vm_uuid, pgnum)

    snapshot_list = []

    for result in results:
        snapshot_tmp = {
            'id': result.id,
            'name': result.name,
            'mor_name': result.mor_name,
            'vm_uuid': result.vm_uuid,
            'description': result.description,
            'state': result.state,
            'snapshot_id': result.snapshot_id,
            'snapshot_parent_id': result.snapshot_parent_id,
            'current': result.current,
            'create_time': result.create_time,
        }
        snapshot_list.append(snapshot_tmp)
    return snapshot_list, pg
