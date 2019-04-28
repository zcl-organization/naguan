# -*- coding:utf-8 -*-
from app.models import VCenterVm
from app.exts import db

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


# 添加vcenter tree 信息
def vcenter_vm_create(uuid, platform_id, vm_name, vm_mor_name, template, vm_path_name, memory, cpu,
                      num_ethernet_cards, num_virtual_disks, instance_uuid, guest_id, guest_full_name, host, ip,
                      status):
    # print(options)
    new_vm = VCenterVm()
    new_vm.platform_id = platform_id
    new_vm.vm_name = unicode(vm_name)
    new_vm.vm_mor_name = vm_mor_name
    new_vm.template = template
    new_vm.vm_path_name = unicode(vm_path_name)
    new_vm.memory = memory
    new_vm.cpu = cpu
    new_vm.num_ethernet_cards = num_ethernet_cards
    new_vm.num_virtual_disks = num_virtual_disks
    new_vm.uuid = uuid
    new_vm.instance_uuid = instance_uuid
    new_vm.guest_id = guest_id
    new_vm.guest_full_name = guest_full_name
    new_vm.host = host
    new_vm.ip = ip
    new_vm.status = status

    db.session.add(new_vm)
    db.session.commit()


def vcenter_get_vm_by_uuid(uuid, platform_id):
    if uuid and platform_id:

        query = db.session.query(VCenterVm)
        return query.filter_by(uuid=uuid).filter_by(platform_id=platform_id).first()
    else:
        return False


def vcenter_update_vm_by_uuid(uuid, platform_id, vm_name, vm_mor_name, template, vm_path_name, memory, cpu,
                              num_ethernet_cards, num_virtual_disks, instance_uuid, guest_id, guest_full_name, host,
                              ip, status):
    if uuid and platform_id:
        vm_info = db.session.query(VCenterVm).filter_by(uuid=uuid).filter_by(platform_id=platform_id).first()
        vm_info.vm_name = unicode(vm_name)
        vm_info.vm_mor_name = vm_mor_name
        vm_info.template = template
        vm_info.vm_path_name = unicode(vm_path_name)
        vm_info.memory = memory
        vm_info.cpu = cpu
        vm_info.num_ethernet_cards = num_ethernet_cards
        vm_info.num_virtual_disks = num_virtual_disks
        vm_info.num_virtual_disks = instance_uuid
        vm_info.guest_id = guest_id
        vm_info.guest_full_name = guest_full_name
        vm_info.host = host
        vm_info.ip = ip
        vm_info.status = status

        db.session.commit()
    else:
        return False


def vcenter_get_vm_by_platform_id(platform_id, host):
    if platform_id and host:
        result = db.session.query(VCenterVm.uuid).filter_by(platform_id=platform_id).filter_by(host=host).all()
        db.session.remove()
        return result
    else:
        return False


def vm_delete_by_uuid(platform_id, host, uuid):
    query = db.session.query(VCenterVm)
    vm_willdel = query.filter_by(platform_id=platform_id).filter_by(host=host).filter_by(uuid=uuid).first()
    db.session.delete(vm_willdel)
    db.session.commit()
    return True


def vm_list(platform_id, host, vm_name):
    query = db.session.query(VCenterVm)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if host:
        query = query.filter_by(host=host)
    if vm_name:
        query = query.filter_by(vm_name=vm_name)
    return query.all()


def list_by_uuid(platform_id, uuid):
    return db.session.query(VCenterVm).filter_by(platform_id=platform_id).filter_by(
        uuid=uuid).first()
