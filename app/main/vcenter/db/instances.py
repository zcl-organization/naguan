# -*- coding:utf-8 -*-
from sqlalchemy import desc, asc
from app.models import VCenterVm
from app.exts import db


# 添加vcenter tree 信息
def vcenter_vm_create(uuid, platform_id, vm_name, vm_mor_name, template, vm_path_name, memory, cpu,
                      num_ethernet_cards, num_virtual_disks, instance_uuid, guest_id, guest_full_name, host, ip,
                      status, resource_pool_name, created_at):
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
    new_vm.resource_pool_name = resource_pool_name
    new_vm.created_at = created_at
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
                              ip, status, resource_pool_name, created_at=None):
    # print('uuid:', uuid)
    # print('platform_id:', platform_id)
    if uuid and platform_id:
        vm_info = db.session.query(VCenterVm).filter_by(uuid=uuid).filter_by(platform_id=platform_id).first()
        # print(vm_info)
        name = vm_name
        vm_info.vm_name = unicode(name)
        vm_info.vm_mor_name = vm_mor_name
        vm_info.template = template
        vm_info.vm_path_name = unicode(vm_path_name)
        vm_info.memory = memory
        vm_info.cpu = cpu
        vm_info.num_ethernet_cards = num_ethernet_cards
        vm_info.num_virtual_disks = num_virtual_disks
        vm_info.instance_uuid = instance_uuid
        vm_info.guest_id = guest_id
        vm_info.guest_full_name = guest_full_name
        vm_info.host = host
        vm_info.ip = ip
        vm_info.status = status
        vm_info.resource_pool_name = resource_pool_name
        # print(created_at)
        if created_at:
            vm_info.created_at = created_at
    try:

        db.session.commit()
    except Exception as e:
        print(str(e))
        raise Exception(e)


def vcenter_get_vm_by_platform_id(platform_id, host):
    if platform_id and host:
        result = db.session.query(VCenterVm.uuid).filter_by(platform_id=platform_id).filter_by(host=host).all()
        # db.session.remove()
        return result
    else:
        return False


def vm_delete_by_uuid(platform_id, host, uuid):
    query = db.session.query(VCenterVm)
    query.filter_by(platform_id=platform_id).filter_by(host=host).filter_by(uuid=uuid).delete(
        synchronize_session=False)


def vm_list(platform_id, host, vm_name, pgnum, pgsort):
    query = db.session.query(VCenterVm)
    if platform_id:
        query = query.filter_by(platform_id=platform_id)
    if host:
        query = query.filter_by(host=host)
    if vm_name:
        query = query.filter_by(vm_name=vm_name)

    if pgsort == 'time':
        query = query.order_by(asc(VCenterVm.created_at))
    else:
        query = query.order_by(desc(VCenterVm.created_at))
    if pgnum:  # 默认获取分页获取所有日志
        query = query.paginate(page=int(pgnum), per_page=10, error_out=False)
    # print(query)
    results = query.items

    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'total': query.total,
        # 'prev_num': query.prev_num,
        # 'next_num': query.next_num,
    }

    return results, pg


def list_by_uuid(platform_id, uuid):
    return db.session.query(VCenterVm).filter_by(platform_id=platform_id).filter_by(
        uuid=uuid).first()


def clean_all_vm_rp_name_by_rp_name(platform_id, rp_name):
    vms = db.session.query(VCenterVm).filter_by(platform_id=platform_id, resource_pool_name=rp_name).all()
    for vm in vms:
        vm.resource_pool_name = None
    db.session.commit()


def update_vm_rp_name_by_vm_mor_name(platform_id, vm_mor_name, rp_name):
    print(rp_name)
    pass
