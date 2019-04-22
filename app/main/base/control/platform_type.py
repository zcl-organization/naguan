# -*- coding:utf-8 -*-
from app.main.base.db import platform_type as db_platform_type


def platform_type_list(options):

    results = db_platform_type.platform_type_list(options)
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


def platform_type_create(options=None):

    # 根据名称判断是否存在类型
    platform_type = db_platform_type.platform_type_list(options)

    if platform_type:
        raise Exception('Existing platform type', options['name'])
    results = db_platform_type.platform_type_create(options)

    if results:
        internal_list = []

        date = {
            'id': results.id,
            'name': results.name,
        }
        internal_list.append(date)
        return internal_list
    else:
        return False


def platform_type_update(id, options=None):

    # p判断是否有云平台信息
    print(id)
    platform = db_platform_type.platform_type_list_by_id(id)
    print(platform)
    if platform:
        return db_platform_type.platform_type_update(id, options)
    else:
        raise Exception('platform type not found', id)


def platform_type_delete(type_id):
    platform = db_platform_type.platform_type_list_by_id(type_id)
    if platform:
        return db_platform_type.platform_type_delete(type_id)
    else:
        raise Exception('platform type not found', type_id)
