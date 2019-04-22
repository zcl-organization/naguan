# -*- coding=utf-8 -*-
import datetime
import uuid
from flask import g
from app.exts import db
from app.models import TaskLog


# 获取日志列表
def log_list_db(options=None):
    query = db.session.query(TaskLog)
    if options['task_id']:
        query = query.filter_by(task_id=options['task_id'])
    if options['rely_task_id']:
        query = query.filter_by(rely_task_id=options['rely_task_id'])
    if options['request_id']:
        query = query.filter_by(request_id=options['request_id'])
    if options['submitter']:
        query = query.filter_by(submitter=options['submitter'])
    if options['page']:  # 默认获取分页获取所有日志
        query = query.paginate(page=options['page'], per_page=20, error_out=False)
    results = query.items
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
    for result in results:
        data = {
            'id': result.id,
            'task_id': result.task_id,
            'request_id': result.request_id,
            'rely_task_id': result.rely_task_id,
            'status': result.status,
            'await_execute': result.await_execute,
            'queue_name': result.queue_name,
            'method_name': result.method_name,
            'submitter': result.submitter,
            'enqueue_time': str(result.enqueue_time),
            'start_time': str(result.start_time),
            'end_time': str(result.end_time),

        }
        result_item.append(data)
    return result_item, pg


# 根据id获取日志
def log_get(id=None):
    result = TaskLog.query.get(id)
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


# 任务日志创建
def task_log_create_db(options):
    newlog = TaskLog()
    newlog.request_id = g.request_id
    newlog.task_id = str(uuid.uuid5(uuid.uuid4(), 'task_log'))
    try:
        newlog.rely_task_id = g.rely_task_id
    except Exception as e:
        newlog.rely_task_id = '--'
    newlog.status = options['result']
    newlog.await_execute = '1' + '/' + '2'
    newlog.queue_name = 'iass_web'   # options['queue_name']  # 暂定
    newlog.method_name = 'task_callback'  # options['method_name']
    newlog.submitter = g.username
    db.session.add(newlog)
    db.session.commit()
    return True


# 开始任务日志
def task_log_start_db(task_id=None):
    query = db.session.query(TaskLog)
    task_log = query.filter_by(task_id=task_id).first()
    if task_log:
        task_log.status = 2
        task_log.start_time = datetime.datetime.now()
        db.session.add(task_log)
        db.session.commit()
        return True
    else:
        return False


# 完成任务日志
def task_log_end_db(task_id=None):
    query = db.session.query(TaskLog)
    task_log = query.filter_by(task_id=task_id).first()
    if task_log:
        task_log.status = 3
        task_log.end_time = datetime.datetime.now()
        db.session.add(task_log)
        db.session.commit()
        return True
    else:
        return False
