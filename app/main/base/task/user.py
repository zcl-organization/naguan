# -*- coding:utf-8 -*-

from app.exts import celery


# @celery.task()
def add(x, y):
    print(x, y)
    return x + y
