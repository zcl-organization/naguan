# -*- coding:utf-8 -*-

from celery import Task
from app.main.base.control import task_logs
from app.exts import celery


class SyncTreeCall(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # 更新任务状态

        task_logs.task_end(task_id, 'ok')
        return super(SyncTreeCall, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print 'task fail'
        task_logs.task_end(task_id, 'failed')
        return super(SyncTreeCall, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery.task(name="TimingSyncTree")
def timing_sync_tree():
    print('periodic task test!!!!!')
    # control.vcenter.sync_tree.apply_async(args=[1], queue='vsphere')
