# -*- coding:utf-8 -*-

from celery import Task
from app.main.vcenter import control
from app.exts import celery

@celery.task(name="TimingSyncTree1")
def timing_sync_tree():
    print('periodic task test!!!!!')
    control.vcenter.sync_tree.apply_async(args=[3], queue='vsphere')