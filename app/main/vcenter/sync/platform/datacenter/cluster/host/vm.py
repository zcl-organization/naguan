# -*- coding=utf-8 -*-
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name

from app.main.vcenter.control.network_devices import sync_network_device
from app.main.vcenter.control.disks import sync_disk
from app.main.vcenter.control.snapshots import sync_snapshot


def sync_vm_instances(platform_id, vm_instances):
    local_data = [
        item.uuid for item in db.instances.get_vm_by_platform_id(platform_id)
    ]

    for vm_instance in vm_instances:
        if not vm_instance.summary.config.uuid:
            continue
        parent = vm_instance.runtime.host
        sync_vm_instance(platform_id, vm_instance, parent)

        sync_network_device(platform_id, vm_instance)
        sync_disk(platform_id, vm_instance)
        sync_snapshot(platform_id, vm_instance)
        if vm_instance.summary.config.uuid in local_data:
            local_data.remove(vm_instance.summary.config.uuid)

    for uuid in local_data:
        db.instances.vm_delete_by_uuid(platform_id, uuid)

        db.network_devices.device_delete_by_vm_uuid(platform_id, uuid)
        db.disks.device_delete_by_vm_uuid(platform_id, uuid)
        db.snapshots.delete_snapshot_by_vm_uuid(uuid)


def sync_vm_instance(platform_id, vm_instance, parent):
    data = dict(
        uuid=vm_instance.summary.config.uuid, 
        platform_id=platform_id,
        vm_name=vm_instance.summary.config.name,
        vm_mor_name=get_mor_name(vm_instance), 
        template=vm_instance.summary.config.template,
        vm_path_name=vm_instance.summary.config.vmPathName,
        memory=vm_instance.summary.config.memorySizeMB,
        cpu=vm_instance.summary.config.numCpu,
        num_ethernet_cards=vm_instance.summary.config.numEthernetCards,
        num_virtual_disks=vm_instance.summary.config.numVirtualDisks,
        instance_uuid=vm_instance.summary.config.instanceUuid,
        guest_id=vm_instance.summary.config.guestId,
        guest_full_name=vm_instance.summary.config.guestFullName,
        host=parent.name, 
        ip=vm_instance.summary.guest.ipAddress if vm_instance.summary.guest else None, 
        status=vm_instance.summary.runtime.powerState,
        resource_pool_name=vm_instance.resourcePool.name if vm_instance.resourcePool else None
    )

    vm_instance_info = db.instances.vcenter_get_vm_by_uuid(vm_instance.summary.config.uuid, platform_id)
    if vm_instance_info:
        db.instances.vcenter_update_vm_by_uuid(**data)
    else:
        data['created_at'] = vm_instance.config.createDate
        db.instances.vcenter_vm_create(**data)
