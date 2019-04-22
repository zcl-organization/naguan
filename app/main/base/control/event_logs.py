# -*- coding=utf-8 -*-
from app.main.base.db.event_logs import log_list_db, log_get, log_delete_db
from app.main.base.db import event_logs as log_manage


# 获取日志列表
def log_list_c(options=None):
    if log_list_db(options):
        result, pg = log_list_db(options)
        return result, pg
    else:
        return False


# 删除日志
def log_delete_c(id=None):
    request_log = log_get(id=id)  # 根据id获取日志
    if request_log:
        result = log_delete_db(id=id)  # 再删除
        if result:
            return True
        else:
            return False
    else:
        return False


# 事件日志创建
# options ={
#  'type': 'menu',
#  'result': ret_status['ok'],
#  'resources_id': '',
#  'event': unicode('获取菜单信息'),
#  'submitter': g.username,
#   }
def eventlog_create(options):
    log_manage.log_create(options)
