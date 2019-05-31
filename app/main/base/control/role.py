# -*- coding:utf-8 -*-
from flask import g

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
        g.error_code = 1302
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
    if not db.role.list_by_id(role_id):
        g.error_code = 1321
        raise Exception('Role information not exists')
    if db.role.role_exist(name):
        g.error_code = 1322
        raise Exception('Role name already exists')
    return db.role.role_update(role_id, name, description)


# 删除角色信息
def role_delete(role_id):
    role = db.role.list_by_id(role_id)
    if not role:
        g.error_code = 1311
        raise Exception('Role information not exists')
    if role.name == 'admin' or 'user':
        g.error_code = 1312
        raise Exception('Unable to delete super administrator role or normal user role')
    return db.role.role_delete(role_id)


def role_list_by_id(role_id):
    try:
        data = role_db.list_by_id(role_id)
        return data
    except Exception as e:
        raise Exception('search user failed')
