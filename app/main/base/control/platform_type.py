# -*- coding:utf-8 -*-
from flask import g

from app.main.base import db


def type_list(id, name):
    results = db.platform_type.platform_type_list(id, name)
    if results:
        internal_list = []
        for result in results:
            date = {
                'id': result.id,
                'name': result.name,
            }
            internal_list.append(date)
        return internal_list
    else:
        return []


def type_create(name):
    # 根据名称判断是否存在类型
    platform_type = db.platform_type.platform_type_list(name=name)

    if platform_type:
        g.error_code = 1502
        raise Exception('Existing platform type', name)
    menu = db.platform_type.platform_type_create(name)
    data_dict = {
        'id': menu.id,
        'name': menu.name,
    }
    return [data_dict]


def type_update(id, name=None):
    # p判断是否有云平台信息
    # print(id)
    platform = db.platform_type.platform_type_list_by_id(id)
    # print(platform)
    if platform:
        return db.platform_type.platform_type_update(id, name)
    else:
        g.error_code = 1521
        raise Exception('platform type not found', id)


def type_delete(type_id):
    platform = db.platform_type.platform_type_list_by_id(type_id)
    if platform:
        return db.platform_type.platform_type_delete(type_id)
    else:
        g.error_code = 1511
        raise Exception('platform type not found', type_id)
