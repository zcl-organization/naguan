# -*- coding=utf-8 -*-
from app.main.base.db.task_logs import log_list_db, log_get, log_delete_db, task_log_start_db, task_log_end_db
from app.main.base.db import task_logs as log_manage


# 获取日志列表
def log_list_c(options=None):
    if log_list_db(options):
        result, pg = log_list_db(options)
        return result, pg
    else:
        return False


# 删除日志
def log_delete_c(id=None):
    task_logs = log_get(id=id)  # 先获取再删除
    if task_logs:
        result = log_delete_db(id=id)
        if result:
            return True
        else:
            return False
    else:
        return False


def task_log_create(options):
    log_manage.task_log_create_db(options)


# 开始任务日志
def task_log_start_c(task_id=None):
    return task_log_start_db(task_id)


# 完成任务日志
def task_log_en_c(task_id=None):
    return task_log_end_db(task_id)









