# -*- coding:utf-8 -*-

from app.models import CloudPlatformType
from app.exts import db
from sqlalchemy.exc import IntegrityError

def platform_type_list(options):
    # noinspection PyBroadException
    try:
        query = db.session.query(CloudPlatformType)
        if options.get('id'):
            query = query.filter_by(id=options.get('id'))
        if options['name']:
            query = query.filter_by(name=options['name'])
        result = query.all()
    except Exception, e:
        result = []

    return result


def platform_type_create(options):
    # noinspection PyBroadException
    try:
        new_platform_type = CloudPlatformType()
        new_platform_type.name = options.get('name')

        db.session.add(new_platform_type)
        db.session.commit()
        platform_type = db.session.query(CloudPlatformType).filter_by(name=options.get('name')).first()
    except Exception, e:
        return Exception('create platform_type error', options.get('name'))

    return platform_type


def platform_type_list_by_id(id):
    platform_type = db.session.query(CloudPlatformType).filter_by(id=id).first()
    return platform_type


def platform_type_update(id, options):
    try:
        platform = db.session.query(CloudPlatformType).filter_by(id=id).first()
        if options.get('name'):
            platform.name = options.get('name')
        db.session.commit()
        return True
    except IntegrityError:
        raise Exception('db update, parameter error',  options.get('name'))
    except Exception as ex:
        return False


def platform_type_delete(type_id):
    try:
        query = db.session.query(CloudPlatformType)
        platform_willdel = query.filter_by(id=type_id).first()
        db.session.delete(platform_willdel)
        db.session.commit()

    except Exception:
        raise Exception('删除云平台类型失败', type_id)
    return True
