# -*- coding:utf-8 -*-
from app.main.vcenter.db import network_devices as db_network
# from app.main.vcenter import db
from pyVmomi import vim


# 同步云主机 network device
def sync_network_device(platform_id, vm):
    devs = vm.config.hardware.device

    device_label = db_network.device_label_all_by_uuid(platform_id=platform_id, vm_uuid=vm.summary.config.uuid)
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
                db_network.device_update(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                         mac=virtual_nic_device.macAddress,
                                         label=virtual_nic_device.deviceInfo.label,
                                         network_port_group=virtual_nic_device.deviceInfo.summary,
                                         address_type=virtual_nic_device.addressType)
            else:
                db_network.device_create(platform_id=platform_id, vm_uuid=vm.summary.config.uuid,
                                         mac=virtual_nic_device.macAddress,
                                         label=virtual_nic_device.deviceInfo.label,
                                         network_port_group=virtual_nic_device.deviceInfo.summary,
                                         address_type=virtual_nic_device.addressType)

    # 删除多余的设备
    if device_labels:
        for device in device_labels:
            db_network.device_delete_by_label(platform_id=platform_id, vm_uuid=vm.summary.config.uuid, label=device)
        print(device_labels)


def device_list_by_id(platform_id, vm_uuid, device_id):
    return db_network.device_list_by_id(platform_id, vm_uuid, device_id)
