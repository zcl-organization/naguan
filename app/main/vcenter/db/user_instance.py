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
    query = db.session.query(VCenterVm.uuid.label('vm_uuid'), UsersInstances.user_id.label('user_id')).filter(
        VCenterVm.template == template).outerjoin(VCenterVm, UsersInstances.vm_id == VCenterVm.uuid)

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
    if user_id:
        query.filter(UsersInstances.user_id.in_(user_id))
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
