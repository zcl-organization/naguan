# -*- coding=utf-8 -*-
from app.exts import db
from app.models import EventLog, Users, Menu, CloudPlatform, CloudPlatformType, Roles, RolesUsers
from flask import g


# 获取日志列表
def log_list(pgnum, event_request_id, task_request_id, submitter, operation_resources_id):

    query = db.session.query(EventLog).order_by(EventLog.time.desc())
    if event_request_id:
        query = query.filter_by(event_request_id=event_request_id)
    if task_request_id:
        query = query.filter_by(task_request_id=task_request_id)
    if operation_resources_id:
        query = query.filter_by(operation_resources_id=operation_resources_id)
    if submitter:
        query = query.filter_by(submitter=submitter)
    if pgnum:  # 默认获取分页获取所有日志
        query = query.paginate(page=pgnum, per_page=10, error_out=False)
    results = query.items
    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'total': query.total,
        # 'prev_num': query.prev_num,
        # 'next_num': query.next_num,
    }

    return results, pg


def log_list_by_id(log_id):
    return db.session.query(EventLog).filter_by(id=log_id).first()


# 删除日志,根据请求id
def log_delete(log_id):
    try:
        query = db.session.query(EventLog)
        log_middle = query.filter_by(id=log_id).first()
        db.session.delete(log_middle)
        db.session.commit()
    except Exception as e:
        g.error_code = 1812
        raise Exception('Database delete exception')


# 事件日志创建
def log_create(type, result, resources_id, event, submitter):
    new_log = EventLog()
    new_log.event_request_id = g.request_id

    new_log.resource_type = type
    new_log.result = result
    new_log.operation_resources_id = str(resources_id)
    new_log.operation_event = event
    new_log.submitter = submitter
    # newlog.time = options['result']
    # print('event_log:', g.event_request_id)
    db.session.add(new_log)
    db.session.commit()
    # return True




