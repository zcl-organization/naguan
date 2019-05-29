# -*- coding:utf-8 -*-

from app.exts import celery
from app.main.vcenter import control


@celery.task(name="TimingSyncTree1")
def timing_sync_tree():
    print('periodic task test!!!!!')
    control.vcenter.sync_tree.apply_async(args=[1], queue='vsphere')
