# -*- coding:utf-8 -*-
from app.models import Roles
from app.exts import db


# 查找是否存在角色
def role_exist(name=None):
    query = db.session.query(Roles)
    query = query.filter_by(name=name).first()
    if query:
        return True
    else:
        return False


# 角色列表
def role_list_db(options=None):
    query = db.session.query(Roles)
    if options['name']:  # 如果存在name，搜索符合name的数据
        query = query.filter_by(name=options['name'])
    if options['pgnum']:  # 默认获取分页获取所有日志,
        query = query.paginate(page=options['pgnum'], per_page=20, error_out=False)
    results = query.items
    data = []
    if results:

        for results in results:
            role_tmp = {
                'id': results.id,
                'name': results.name,
                'description': results.description,
            }
            data.append(role_tmp)
    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'total': query.total,
        # 'prev_num': query.prev_num,
        # 'next_num': query.next_num,
    }
    return data, pg


# 创建角色信息
def role_create_db(options=None):
    if not options['name']:
        return False
    else:
        res = role_exist(options['name'])
        if res:
            return False
        else:
            role = Roles()
            role.name = options['name']
            role.description = options['description']
            db.session.add(role)
            db.session.commit()
            return role.name


# 更新角色信息
def role_update_db(options=None):
    role = Roles.query.get(options['id'])
    if role:
        role_re = Roles.query.filter_by(name=options['name']).first()
        if role_re and role != role_re:
            return False
        else:
            role.name = options['name']
            role.description = options['description']
            db.session.add(role)
            db.session.commit()
            return True
    else:
        return False


# 删除角色信息
def role_delete_db(id=None):
    role = Roles.query.get(id)
    if role:
        name = role.name
        db.session.delete(role)
        db.session.commit()
        return name
    else:
        return False


def list_by_id(role_id):
    data = db.session.query(Roles).filter(Roles.id == role_id).first()
    return data
