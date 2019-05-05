# -*- coding=utf-8 -*-
from app.exts import db
from app.models import RequestLog


# 获取日志列表
def log_list(pgnum, request_id, status_num):
    query = db.session.query(RequestLog)
    if request_id:
        query = query.filter_by(request_id=request_id)
    if status_num:
        query = query.filter_by(status_num=status_num)
    if pgnum:  # 默认获取分页获取所有日志
        query = query.paginate(page=pgnum, per_page=10, error_out=False)
    results = query.items
    print(results)

    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'total': query.total,
        # 'prev_num': query.prev_num,
        # 'next_num': query.next_num,
    }

    return results, pg


# 删除日志,根据请求id
def log_delete(id):
    try:
        query = db.session.query(RequestLog)
        log_willdel = query.filter_by(id=id).first()
        db.session.delete(log_willdel)
        db.session.commit()
    except Exception as e:
        raise Exception('Database delete exception')


def log_list_by_id(id):
    return db.session.query(RequestLog).filter_by(id=id).first()

