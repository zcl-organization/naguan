# -*- coding=utf-8 -*-


# 获取系统配置
from app.main.base.db import system as db_system


def system_list():
    systems = db_system.system_list()
    if systems:
        return systems
    else:
        return False


def system_list_put(data):
    systems = db_system.system_list()
    if systems:
        system = systems[0]
        if data.get('platform_name'):
            system.platform_name = data.get('platform_name').decode("utf-8")
        if data.get('version_information'):
            system.version_information = data.get('version_information').decode("utf-8")
        if data.get('copyright'):
            system.copyright = data.get('copyright').decode("utf-8")
        if data.get('user_authentication_mode'):
            system.user_authentication_mode = data.get('user_authentication_mode').decode("utf-8")
        if data.get('debug') == 0:
            system.debug = False
        elif data.get('debug') == 1:
            system.debug = True
        else:  # '请重新输入debug（1代表True，0代表False)'
            return False
        db_system.system_save_db(system)
        return system
    else:
        return False


def system_save(system):
    return db_system.system_save_db(system)


def system_get(sysconfig):
    return db_system.system_get(sysconfig)