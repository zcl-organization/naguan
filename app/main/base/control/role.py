# -*- coding:utf-8 -*-

from app.main.base.db import role as role_db
from app.main.base import db


# 角色列表
def role_list(name, pgnum):
    results, pg = db.role.role_list(name, pgnum)

    data = []
    for results in results:
        role_tmp = {
            'id': results.id,
            'name': results.name,
            'description': results.description,
        }
        data.append(role_tmp)
    return data, pg


# 创建角色信息
def role_create(name, description):
    if db.role.role_exist(name):
        raise Exception('Role information already exists')
    data = db.role.role_create(name, description)
    role_dict = {
        'id': data.id,
        'name': data.name,
        'description': data.description,
    }
    return [role_dict]


# 更新角色信息
def role_update(role_id, name, description):
    role = db.role.list_by_id(role_id)
    if not role:
        raise Exception('Role information not exists')
    if role.name == 'admin' or role.name == 'user':
        raise Exception('Unable to update super administrator role or normal user role')
    if db.role.role_exist(name) and role.name != name:
        raise Exception('Role name already exists')
    return db.role.role_update(role_id, name, description)


# 删除角色信息
def role_delete(role_id):
    role = db.role.list_by_id(role_id)
    if not role:
        raise Exception('Role information not exists')
    if role.name == 'admin' or role.name == 'user':
        raise Exception('Unable to delete super administrator role or normal user role')

    # 删除用户角色信息
    db.roles_users.delete_role_by_role_id(role_id)
    # 删除菜单权限信息
    db.roles_menus.delete_by_role_id(role_id)
    # 删除菜单
    db.role.role_delete(role_id)
    return role


def role_list_by_id(role_id):
    try:
        return role_db.list_by_id(role_id)
    except Exception as e:
        raise Exception('search user failed')
