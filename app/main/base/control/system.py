# -*- coding=utf-8 -*-
import os

from flask import g

from app.main.base import db
from config import UPLOAD_DIR


def system_config_list():
    system = db.system.system_config_list()
    if not system:
        g.error_code = 1752
        raise Exception('System information is not configured')
    data = [{
        'id': system.id,
        'platform_name': system.platform_name,
        'version': system.version_information,
        'copyright': system.copyright,
        'user_authentication_mode': system.user_authentication_mode,
        'debug': system.debug,
    }]
    return data


def system_config_update(platform_name, version_information, copyright, user_authentication_mode, debug):
    system = db.system.system_config_list()
    if system:
        db.system.system_config_update(platform_name, version_information, copyright, user_authentication_mode, debug)
    else:
        g.error_code = 1782
        raise Exception('System information is not configured')


def system_config_create(platform_name, version_information, copyright, user_authentication_mode, debug):
    system = db.system.system_config_list()
    if system:
        system_config_update(platform_name, version_information, copyright, user_authentication_mode, debug)
    else:
        db.system.system_config_create(platform_name, version_information, copyright, user_authentication_mode, debug)
    # return db.system.system_save(system)


def system_config_update_logo(logo):
    logo_name = logo.filename
    logo_path = os.path.join(UPLOAD_DIR, logo_name)

    system = db.system.system_config_list()
    if not system:
        g.error_code = 1712
        raise Exception('System information is not configured')

    logo.save(logo_path)

    path = UPLOAD_DIR + logo_name
    # print(path)
    db.system.system_config_update_logo(path)
