# -*- coding=utf-8 -*-
import datetime
import uuid
from flask import g
from app.exts import db
from app.models import TaskLog


# 获取日志列表
def log_list(pgnum, task_id, rely_task_id, submitter, request_id):
    query = db.session.query(TaskLog)
    if task_id:
        query = query.filter_by(task_id=task_id)
    if rely_task_id:
        query = query.filter_by(rely_task_id=rely_task_id)
    if request_id:
        query = query.filter_by(request_id=request_id)
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
        'prev_num': query.prev_num,
        'next_num': query.next_num,
    }

    return results, pg


def log_list_by_id(log_id):
    return db.session.query(TaskLog).filter_by(id=log_id).first()


# 删除日志,根据请求id
def log_delete(log_id):
    try:
        query = db.session.query(TaskLog)
        log_middle = query.filter_by(id=log_id).first()
        db.session.delete(log_middle)
        db.session.commit()
    except Exception as e:
        raise Exception('Database delete exception')


# 任务日志创建
def create_log(task_id, state, queue, task):
    newlog = TaskLog()
    newlog.request_id = g.request_id
    newlog.task_id = task_id
    try:
        newlog.rely_task_id = g.rely_task_id
    except Exception as e:
        newlog.rely_task_id = '--'
    newlog.status = state
    newlog.await_execute = '1' + '/' + '2'
    newlog.queue_name = queue
    newlog.method_name = task
    newlog.submitter = g.username
    db.session.add(newlog)
    db.session.commit()
    return True


# 更新任务日志状态
def task_update(task_id, action, state):
    query = db.session.query(TaskLog)
    task_log = query.filter_by(task_id=task_id).first()
    if task_log:

        task_log.status = state

        if action == 'start':
            task_log.start_time = datetime.datetime.now()
        else:
            task_log.end_time = datetime.datetime.now()
        db.session.add(task_log)
        db.session.commit()
