# -*- coding:utf-8 -*-
from app.main.vcenter.db import network_devices as db_network
from app.main.vcenter import db
from pyVmomi import vim


# 同步云主机 network device
def sync_network_device(platform_id, vm):
    devs = vm.config.hardware.device

    device_label = db.network_devices.device_label_all_by_uuid(platform_id=platform_id, vm_uuid=vm.summary.config.uuid)
    device_labels = []
    for device in device_label:
        device_labels.append(device.label)

    for dev in devs:
        virtual_nic_device = None
        # db_network.network_device_info_create(platform_id, )
        nic_label = 'Network adapter'
        if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
                and nic_label in dev.deviceInfo.label:
            virtual_nic_device = dev

        if virtual_nic_device:
            if virtual_nic_device.deviceInfo.label in device_labels:
                device_labels.remove(virtual_nic_device.deviceInfo.label)
                db.network_devices.device_update(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                                 mac=virtual_nic_device.macAddress,
                                                 label=virtual_nic_device.deviceInfo.label,
                                                 network_port_group=virtual_nic_device.deviceInfo.summary,
                                                 address_type=virtual_nic_device.addressType)
            else:
                db.network_devices.device_create(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                                 mac=virtual_nic_device.macAddress,
                                                 label=virtual_nic_device.deviceInfo.label,
                                                 network_port_group=virtual_nic_device.deviceInfo.summary,
                                                 address_type=virtual_nic_device.addressType)

    # 删除多余的设备
    if device_labels:
        for device in device_labels:
            db.network_devices.device_delete_by_label(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                                      label=device)
        print(device_labels)


def device_list_by_id(platform_id, vm_uuid, device_id):
    return db.network_devices.device_list_by_id(platform_id, vm_uuid, device_id)


def get_network_by_vm_uuid(platform_id, vm_uuid):
    network_devices = db.network_devices.get_network_by_vm_uuid(platform_id, vm_uuid)

    network_device_list = []
    for device in network_devices:
        device_tmp = {
            'id': device.id,
            'platform_id': device.platform_id,
            'vm_uuid': device.vm_uuid,
            'label': device.label,
            'mac': device.mac,
            'network_port_group': device.network_port_group,
            'address_type': device.address_type,
        }
        network_device_list.append(device_tmp)
    return network_device_list
