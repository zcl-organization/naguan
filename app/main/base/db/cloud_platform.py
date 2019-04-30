# -*- coding:utf-8 -*-

from app.models import CloudPlatform
from app.exts import db


def platform_list(id=None, platform_name=None, platform_type_id=None):
    query = db.session.query(CloudPlatform)
    # print(options)
    try:
        if id:
            query = query.filter_by(id=id)
            # print('query2:', query)
        if platform_name:
            query = query.filter_by(platform_name=platform_name)
        if platform_type_id:
            query = query.filter_by(platform_type_id=platform_type_id)
        result = query.all()
    except Exception as e:
        raise Exception('Database operation exception')
    return result


# 添加第三方云平台
def platform_create(options):
    # print(options)
    new_platform = CloudPlatform()
    try:
        new_platform.platform_type_id = options['platform_type_id']
        new_platform.platform_name = options['platform_name']
        new_platform.ip = options['ip']
        new_platform.port = options['port']
        new_platform.admin_name = options['admin_name']
        new_platform.admin_password = options['admin_password']
        new_platform.remarks = options['remarks']

        db.session.add(new_platform)
        db.session.commit()
        # return db.session.query(CloudPlatform).filter_by(platform_name=options['platform_name']).first()
        return True
    except Exception, e:
        return False


def platform_update(id, options):
    try:
        platform = db.session.query(CloudPlatform).filter_by(id=id).first()
        if options['ip']:
            platform.ip = options['ip']
        if options['port']:
            platform.port = options['port']
        if options['admin_name']:
            platform.admin_name = options['admin_name']
        if options['admin_password']:
            platform.admin_name = options['admin_password']
        if options['remarks']:
            platform.admin_name = options['remarks']
        db.session.commit()
        return True
    except Exception, e:
        return False


def platform_list_by_id(id):
    return db.session.query(CloudPlatform).filter_by(id=id).first()


def platform_delete(id):
    query = db.session.query(CloudPlatform)
    platform_willdel = query.filter_by(id=id).first()
    db.session.delete(platform_willdel)
    db.session.commit()
    return True
