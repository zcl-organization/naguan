# -*- coding=utf-8 -*-
from flask import g

from app.main.base import db


# 获取日志列表
def log_list(pgnum, request_id, status_num):

    results, pg = db.request_logs.log_list(pgnum, request_id, status_num)
    # print(pg)
    data = []
    for request in results:
        data_tmp = {
            'id': request.id,
            'request_id': request.request_id,
            'ip': request.ip,
            'url': request.url,
            'status': request.status_num,
            'submitter': request.submitter,
            'time': request.time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        data.append(data_tmp)
    return data, pg


def log_delete(id):
    log = db.request_logs.log_list_by_id(id)
    if not log:
        g.error_code = 1711
        raise Exception('No current log information exists')
    return db.request_logs.log_delete(id)
