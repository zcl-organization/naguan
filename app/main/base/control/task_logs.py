# -*- coding=utf-8 -*-
from app.main.base import db


# 获取日志列表
def log_list(pgnum, task_id, rely_task_id, submitter, request_id):
    results, pg = db.task_logs.log_list(pgnum, task_id, rely_task_id, submitter, request_id)
    # print(results)
    # print(pg)
    data = []
    if results:
        for result in results:
            data_tmp = {
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
            data.append(data_tmp)
    return data, pg


# 删除日志
def log_delete(log_id):
    log = db.task_logs.log_list_by_id(log_id)
    if not log:
        raise Exception('No current log information exists')
    return db.task_logs.log_delete(log_id)


def create_log(request_id, task_id, state, queue, task):
    db.task_logs.create_log(request_id, task_id, state, queue, task)


# 开始任务日志
def task_start(task_id, state):
    return db.task_logs.task_update(task_id, 'start', state)


# 完成任务日志
def task_end(task_id, state):
    return db.task_logs.task_update(task_id, 'end', state)
