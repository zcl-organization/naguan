# -*- coding=utf-8 -*-
from app.main.base import db


# 获取日志列表
def log_list(pgnum, event_request_id, task_request_id, submitter, operation_resources_id):
    results, pg = db.event_logs.log_list(pgnum, event_request_id, task_request_id, submitter, operation_resources_id)

    data = []
    for result in results:
        data_temp = {
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
        data.append(data_temp)
    return data, pg


# 删除日志
def log_delete(log_id):
    log = db.event_logs.log_list_by_id(log_id)
    if not log:
        raise Exception('No current log information exists')
    return db.event_logs.log_delete(log_id)


# 事件日志创建
# options ={
#  'type': 'menu',
#  'result': ret_status['ok'],
#  'resources_id': '',
#  'event': unicode('获取菜单信息'),
#  'submitter': g.username,
#   }
def eventlog_create(type, result, resources_id, event, submitter):
    db.event_logs.log_create(type, result, resources_id, event, submitter)
