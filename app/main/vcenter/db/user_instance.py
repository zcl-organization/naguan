from sqlalchemy import desc, asc
from app.exts import db
from app.models import UsersInstances, VCenterVm


def assignment_vm_to_user(user_id, vm_uuid, platform_id):
    new_user_instance = UsersInstances()
    new_user_instance.user_id = user_id
    new_user_instance.vm_id = vm_uuid
    new_user_instance.platform_id = platform_id

    db.session.add(new_user_instance)
    db.session.commit()


def get_vm_list_by_user_ids(platform_id, host, vm_name, pgnum, pgsort, template=None, user_id=None):
    query = db.session.query(VCenterVm.id.label('id'), VCenterVm.platform_id.label('platform_id'),
                             VCenterVm.vm_name.label('vm_name'), VCenterVm.vm_mor_name.label('vm_mor_name'),
                             VCenterVm.template.label('template'), VCenterVm.vm_path_name.label('vm_path_name'),
                             VCenterVm.memory.label('memory'), VCenterVm.cpu.label('cpu'),
                             VCenterVm.num_ethernet_cards.label('num_ethernet_cards'),
                             VCenterVm.num_virtual_disks.label('num_virtual_disks'),
                             VCenterVm.instance_uuid.label('instance_uuid'),
                             VCenterVm.uuid.label('uuid'), VCenterVm.guest_id.label('guest_id'),
                             VCenterVm.guest_full_name.label('guest_full_name'), VCenterVm.host.label('host'),
                             VCenterVm.guest_id.label('guest_id'), VCenterVm.ip.label('ip'),
                             VCenterVm.created_at.label('created_at'),
                             VCenterVm.status.label('status'), UsersInstances.user_id.label('user_id')).filter(
        VCenterVm.template == template).outerjoin(UsersInstances, UsersInstances.vm_id == VCenterVm.uuid)

    if platform_id:
        query = query.filter(VCenterVm.platform_id == platform_id)
    if host:
        query = query.filter(VCenterVm.host == host)
    if vm_name:
        query = query.filter(VCenterVm.vm_name == vm_name)

    if pgsort == 'time':
        query = query.order_by(asc(VCenterVm.created_at))
    else:
        query = query.order_by(desc(VCenterVm.created_at))
    # if user_id:
    query = query.filter(UsersInstances.user_id.in_(user_id))
    if pgnum:
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
