# -*- coding:utf-8 -*-
from celery import Task
from app.main.base.control import task_logs


class call_sync_tree(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # 更新任务状态

        task_logs.task_end(task_id, 'ok')

        return super(call_sync_tree, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print 'task fail, reason'
        task_logs.task_end(task_id, 'failed')
        return super(call_sync_tree, self).on_failure(exc, task_id, args, kwargs, einfo)
