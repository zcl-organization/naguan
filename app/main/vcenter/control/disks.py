# -*- coding:utf-8 -*-
from app.main.vcenter import db
from pyVmomi import vim


# 同步云主机 network device
def sync_disk(platform_id, vm):
    devs = vm.config.hardware.device

    # 获取云主机所有的硬盘信息

    # device_label = db_network.device_label_all_by_uuid(platform_id=platform_id, vm_uuid=vm.summary.config.uuid)
    disk_uuid = db.disks.get_disk_uuid_by_vm_uuid(platform_id=platform_id, vm_uuid=vm.summary.config.uuid)
    device_uuids = []
    for device in disk_uuid:
        device_uuids.append(device.disk_uuid)

    for dev in devs:
        disk_device = None

        dev_label = dev.deviceInfo.label
        if dev_label.startswith('Hard disk'):

            try:
                res = dev.vFlashCacheConfigInfo.reservationInMB
            except Exception as e:
                res = 0

            if dev.backing.thinProvisioned:
                types = 'thinProvisioned'
            else:
                types = 'Provisioned'

            if dev.backing.uuid in device_uuids:
                device_uuids.remove(dev.backing.uuid)
                db.disks.disk_update(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                     label=dev.deviceInfo.label,
                                     disk_size=dev.deviceInfo.summary, disk_file=dev.backing.fileName,
                                     level=dev.shares.level, shares=dev.shares.shares,
                                     iops=dev.storageIOAllocation.limit, cache=res, disk_type=types,
                                     sharing=dev.backing.sharing, disk_mode=dev.backing.diskMode,
                                     disk_uuid=dev.backing.uuid)
            else:

                db.disks.disk_create(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                     label=dev.deviceInfo.label,
                                     disk_size=dev.deviceInfo.summary, disk_file=dev.backing.fileName,
                                     level=dev.shares.level, shares=dev.shares.shares,
                                     iops=dev.storageIOAllocation.limit, cache=res, disk_type=types,
                                     sharing=dev.backing.sharing, disk_mode=dev.backing.diskMode,
                                     disk_uuid=dev.backing.uuid)

    # 删除多余的设备
    if device_uuids:
        for device in device_uuids:
            db.disks.device_delete_by_uuid(platform_id=platform_id, disk_uuid=device)


def get_disk_by_vm_uuid(platform_id, vm_uuid):
    disks = db.disks.get_disk_by_vm_uuid(platform_id, vm_uuid)
    disk_list = []
    for disk in disks:
        print(disk.id)
        ds_tmp = {
            'id': disk.id,
            'platform_id': platform_id,
            'vm_uuid': disk.vm_uuid,
            'disk_uuid': disk.disk_uuid,
            'label': disk.label,
            'disk_size': disk.disk_size,
            'disk_type': disk.disk_type,
            'sharing': disk.sharing,
            'disk_file': disk.disk_file,
            'shares': disk.shares,
            'level': disk.level,
            'iops': disk.iops,
            'cache': disk.cache,
            'disk_mode': disk.disk_mode,
        }
        disk_list.append(ds_tmp)
    return disk_list
