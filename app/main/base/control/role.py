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
    return db.role.role_create(name, description)


# 更新角色信息
def role_update(role_id, name, description):
    if not db.role.list_by_id(role_id):
        raise Exception('Role information not exists')
    if db.role.role_exist(name):
        raise Exception('Role name already exists')
    return db.role.role_update(role_id, name, description)


# 删除角色信息
def role_delete(role_id):
    if not db.role.list_by_id(role_id):
        raise Exception('Role information not exists')
    return db.role.role_delete(role_id)


def role_list_by_id(role_id):
    try:
        data = role_db.list_by_id(role_id)
        return data
    except Exception as e:
        raise Exception('search user failed')
