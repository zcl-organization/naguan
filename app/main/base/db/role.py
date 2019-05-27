# -*- coding:utf-8 -*-
from app.models import Roles
from app.exts import db


# 查找是否存在角色
def role_exist(name=None):
    data = db.session.query(Roles).filter_by(name=name).first()
    # query = query.filter_by(name=name).first()
    if data:
        return True
    else:
        return False


# 角色列表
def role_list(name, pgnum):
    try:
        query = db.session.query(Roles)
        if name:  # 如果存在name，搜索符合name的数据
            query = query.filter_by(name=name)
        if pgnum:  # 默认获取分页获取所有日志,
            query = query.paginate(page=pgnum, per_page=20, error_out=False)
        data = query.items

        pg = {
            'has_next': query.has_next,
            'has_prev': query.has_prev,
            'page': query.page,
            'pages': query.pages,
            'total': query.total,
        }
    except Exception as e:
        raise Exception('Database operation exception')
    return data, pg


# 创建角色信息
def role_create(name, description):
    try:

        role = Roles()
        role.name = name
        role.description = description
        db.session.add(role)
        db.session.flush()
        db.session.commit()
        return role
    except Exception as e:
        raise Exception('Database operation exception')


# 更新角色信息
def role_update(role_id, name, description):
    try:
        role = Roles.query.filter_by(id=role_id).first()
        if name:
            role.name = name
        if description:
            role.description = description

        db.session.commit()
        return role.name
    except Exception as e:
        raise Exception('Database operation exception')


# 删除角色信息
def role_delete(role_id):
    query = db.session.query(Roles)
    try:
        role_willdel = query.filter_by(id=role_id).first()
        name = role_willdel.name
        db.session.delete(role_willdel)
        db.session.commit()
        return name
    except Exception as e:
        raise Exception('Database operation exception')


def list_by_id(role_id):

    data = db.session.query(Roles).filter(Roles.id == role_id).first()
    return data


# # 获取资源id
# def get_role():
#     role = db.session.query(Roles).order_by(-Roles.id).first()
#     role_id = role.id
#     return role_id
