# -*- coding:utf-8 -*-

from app.models import CloudPlatform
from app.exts import db


def platform_list(id, platform_type_id, platform_name):
    query = db.session.query(CloudPlatform)
    try:
        if id:
            query = query.filter_by(id=id)
        if platform_name:
            query = query.filter_by(platform_name=platform_name)
        if platform_type_id:
            query = query.filter_by(platform_type_id=platform_type_id)
        result = query.all()
    except Exception as e:
        raise Exception('Database operation exception')
    return result


# 添加第三方云平台
# def platform_create(options):
def platform_create(platform_type_id, platform_name, admin_name, admin_password, port, ip, remarks):
    new_platform = CloudPlatform()
    try:
        new_platform.platform_type_id = platform_type_id
        new_platform.platform_name = platform_name
        new_platform.ip = ip
        new_platform.port = port
        new_platform.admin_name = admin_name
        new_platform.admin_password = admin_password
        new_platform.remarks = remarks

        db.session.add(new_platform)
        db.session.commit()
        # return db.session.query(CloudPlatform).filter_by(platform_name=options['platform_name']).first()

    except Exception as e:
        raise Exception('Database operation exception')


def platform_update(id, ip, admin_name, admin_password, port, remarks):
    try:
        platform = db.session.query(CloudPlatform).filter_by(id=id).first()
        if ip:
            platform.ip = ip
        if port:
            platform.port = port
        if admin_name:
            platform.admin_name = admin_name
        if admin_password:
            platform.admin_password = admin_password
        if remarks:
            platform.remarks = remarks
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation exception')


def platform_list_by_id(id):
    return db.session.query(CloudPlatform).filter_by(id=id).first()


def platform_delete(id):
    try:
        query = db.session.query(CloudPlatform)
        platform_willdel = query.filter_by(id=id).first()
        db.session.delete(platform_willdel)
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation exception')


# 获取资源id
def get_cloud_platform():
    cloud_platform = db.session.query(CloudPlatform).order_by(-CloudPlatform.id).first()
    cloud_id = cloud_platform.id
    return cloud_id
