# -*- coding:utf-8 -*-
from flask import g

from app.models import CloudPlatformType
from app.exts import db
from sqlalchemy.exc import IntegrityError


def platform_type_list(id=None, name=None):
    # noinspection PyBroadException
    try:
        query = db.session.query(CloudPlatformType)
        if id:
            query = query.filter_by(id=id)
        if name:
            query = query.filter_by(name=name)
        result = query.all()
    except Exception as e:
        raise Exception('Database operation exception')

    return result


def platform_type_create(name):
    # noinspection PyBroadException
    try:
        new_platform_type = CloudPlatformType()
        new_platform_type.name = name

        db.session.add(new_platform_type)
        db.session.flush()
        db.session.commit()
        return new_platform_type
    except Exception as e:
        g.error_code = 1503
        raise Exception('create platform_type error', name)

    # return platform_type


def platform_type_list_by_id(id):
    platform_type = db.session.query(CloudPlatformType).filter_by(id=id).first()
    return platform_type


def platform_type_update(id, name):
    try:
        platform = db.session.query(CloudPlatformType).filter_by(id=id).first()
        if name:
            platform.name = name
        db.session.commit()

    except IntegrityError:
        g.error_code = 1524
        raise Exception('db update, parameter error', name)
    except Exception as e:
        g.error_code = 1522
        raise Exception('Database operation exception')


def platform_type_delete(type_id):
    try:
        query = db.session.query(CloudPlatformType)
        platform_middle = query.filter_by(id=type_id).first()
        db.session.delete(platform_middle)
        db.session.commit()
    except Exception:
        g.error_code = 1512
        raise Exception('Deleting platform type failed', type_id)


# # 获取资源id
# def get_platform_type():
#     cloud_platform_type = db.session.query(CloudPlatformType).order_by(-CloudPlatformType.id).first()
#     cloud_type_id = cloud_platform_type.id
#     return cloud_type_id
