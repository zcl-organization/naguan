# -*- coding:utf-8 -*-
from flask import g

from app.main.base import db


# def platform_create(options):
def platform_create(platform_type_id, platform_name, admin_name, admin_password, port, ip, remarks):
    platform = db.cloud_platform.get_platform_by_name(platform_name)

    if platform:
        g.error_code = 1502
        raise Exception('platform name already exist.')
    data = db.cloud_platform.platform_create(platform_type_id, platform_name, admin_name, admin_password, port, ip,
                                             remarks)
    platform_dict = {
        'id': data.id,
        'platform_type_id': data.platform_type_id,
        'platform_name': data.platform_name,
        'ip': data.ip,
        'port': data.port,
        'name': data.admin_name,
        'remarks': data.remarks
    }
    return [platform_dict]


def platform_list(id=None, platform_type_id=None, platform_name=None, platform_type_name=None):
    platforms = db.cloud_platform.platform_list(id, platform_type_id, platform_name, platform_type_name)
    platforms_list = []

    if platforms:
        for platform in platforms:
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
    return platforms_list

def platform_by_id(platform_id):
    datas = platform_list(id=platform_id) 
    return datas[0] if len(datas) == 1 else None


# def platform_update(id, options=None):
def platform_update(id, ip, admin_name, admin_password, port, remarks):
    # 判断是否有云平台信息
    platform = db.cloud_platform.platform_list_by_id(id)
    if platform:
        return db.cloud_platform.platform_update(id, ip, admin_name, admin_password, port, remarks)
    else:
        g.error_code = 1521
        raise Exception('No current platform information exists')


def platform_delete(id):
    platform = db.cloud_platform.platform_list_by_id(id)
    if platform:
        return db.cloud_platform.platform_delete(id)
    else:
        g.error_code = 1511
        raise Exception('No current platform information exists')
