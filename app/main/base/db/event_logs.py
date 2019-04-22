# -*- coding=utf-8 -*-
from app.exts import db
from app.models import EventLog
from flask import g


# 获取日志列表
def log_list_db(options=None):
    query = db.session.query(EventLog)
    if options['event_request_id']:
        query = query.filter_by(event_request_id=options['event_request_id'])
    if options['task_request_id']:
        query = query.filter_by(task_request_id=options['task_request_id'])
    if options['operation_resources_id']:
        query = query.filter_by(operation_resources_id=options['operation_resources_id'])
    if options['submitter']:
        query = query.filter_by(submitter=options['submitter'])
    if options['page']:  # 默认获取分页获取所有日志
        query = query.paginate(page=options['page'], per_page=20, error_out=False)
    results = query.items
    for result in results:

        pg = {
            'has_next': query.has_next,
            'has_prev': query.has_prev,
            'page': query.page,
            'pages': query.pages,
            'total': query.total,
            'prev_num': query.prev_num,
            'next_num': query.next_num,
        }
        result_item = []
        data = {
            'id': result.id,
            'resource_type': result.resource_type,
            'result': result.result,
            'operation_resources_id': result.operation_resources_id,
            'operation_event': result.operation_event,
            'submitter': result.submitter,
            'time': result.time.strftime('%Y-%m-%d %H:%M:%S'),
            'event_request_id': result.event_request_id,
            'task_request_id': result.task_request_id,
        }
        result_item.append(data)
    return result_item, pg


# 根据id获取日志
def log_get(id=None):
    result = EventLog.query.get(id)
    return result


# 删除日志,根据请求id
def log_delete_db(id=None):
    try:
        log = log_get(id)  # 先获取再删除
        db.session.delete(log)
        db.session.commit()
        return True
    except Exception as e:
        return False


# 事件日志创建
def log_create(options):
    newlog = EventLog()
    newlog.event_request_id = g.request_id

    newlog.resource_type = options['type']
    newlog.result = options['result']
    newlog.operation_resources_id = options['resources_id']
    newlog.operation_event = options['event']
    newlog.submitter = options['submitter']
    # newlog.time = options['result']
    # print('event_log:', g.event_request_id)
    db.session.add(newlog)
    db.session.commit()
    return True
