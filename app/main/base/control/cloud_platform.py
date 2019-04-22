# -*- coding:utf-8 -*-
from app.main.base.db import cloud_platform as db_platform


def platform_create(options):
    return db_platform.platform_create(options)


def platform_list(options=None):
    platforms = db_platform.platform_list(options)
    # print(platforms)
    platforms_list =[]
    # print('platforms:', platforms)
    if platforms:
        for platform in platforms:
            # print('id:',platform.id)
            platform_tmp = {
                'id': platform.id,
                'platform_type_id': platform.platform_type_id,
                'platform_name': platform.platform_name,
                'ip': platform.ip,
                'port': platform.port,
                'name': platform.admin_name,
                'password': platform.admin_password,
                'remarks': platform.remarks
            }
            # print(platform_tmp)
            platforms_list.append(platform_tmp)
        # print(platforms_list)
    # print('platforms_list:', platforms_list)
    return platforms_list


def platform_update(id, options=None):

    # p判断是否有云平台信息
    platform = db_platform.platform_list_by_id(id)
    if platform:
        return db_platform.platform_update(id, options)
    else:
        return False


def platform_delete(id):
    platform = db_platform.platform_list_by_id(id)
    if platform:
        return db_platform.platform_delete(id)
    else:
        return False