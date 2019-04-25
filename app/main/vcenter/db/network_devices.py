# -*- coding:utf-8 -*-
from app.models import VCenterNetworkDevice
from app.exts import db


def device_create(platform_id, vm_uuid, mac, label, network_port_group, address_type):
    # print(platform_id, vm_uuid, mac, label, network_port_group, address_type)

    new_network = VCenterNetworkDevice()
    new_network.platform_id = platform_id
    new_network.vm_uuid = vm_uuid
    new_network.mac = mac
    new_network.label = label
    new_network.network_port_group = network_port_group
    new_network.address_type = address_type

    db.session.add(new_network)
    db.session.commit()


def device_update(platform_id, vm_uuid, label, mac, network_port_group, address_type):
    # print(platform_id, vm_uuid, mac, label, network_port_group, address_type)

    device_info = db.session.query(VCenterNetworkDevice).filter_by(platform_id=platform_id).filter_by(
        vm_uuid=vm_uuid).filter_by(label=label).first()
    device_info.mac = mac
    device_info.network_port_group = network_port_group
    device_info.address_type = address_type

    db.session.commit()


def device_by_uuid_and_label(platform_id, vm_uuid, label):
    device_info = db.session.query(VCenterNetworkDevice).filter_by(platform_id=platform_id).filter_by(
        vm_uuid=vm_uuid).filter_by(label=label).first()
    return device_info


def device_label_all_by_uuid(platform_id, vm_uuid):
    device_info = db.session.query(VCenterNetworkDevice.label).filter_by(
        platform_id=platform_id).filter_by(vm_uuid=vm_uuid).all()
    return device_info


# 根据平台id，vm_uuid,label 删除device
def device_delete_by_label(platform_id, vm_uuid, label):
    query = db.session.query(VCenterNetworkDevice)
    vm_willdel = query.filter_by(platform_id=platform_id).filter_by(vm_uuid=vm_uuid).filter_by(label=label).first()
    db.session.delete(vm_willdel)
    db.session.commit()


# 根据network device id 获取network device 信息
def device_list_by_id(platform_id, vm_uuid, id):
    return db.session.query(VCenterNetworkDevice).filter_by(platform_id=platform_id).filter_by(
        vm_uuid=vm_uuid).filter_by(id=id).first()
