# -*- coding=utf-8 -*-
from app.exts import db
from app.models import RequestLog


# 获取日志列表
def log_list_db(options=None):
    query = db.session.query(RequestLog)
    if options['request_id']:
        query = query.filter_by(request_id=options['request_id'])
    if options['status_num']:
        query = query.filter_by(status_num=options['status_num'])
    if options['page']:  # 默认获取分页获取所有日志
        query = query.paginate(page=options['page'], per_page=20, error_out=False)
    results = query.items

    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'total': query.total,
        'prev_num': query.prev_num,
        'next_num': query.next_num,
    }
    result_item = []
    for request in results:
        data = {
            'id': request.id,
            'request_id': request.request_id,
            'ip': request.ip,
            'url': request.url,
            'status_num': request.status_num,
            'submitter': request.submitter,
            'time': request.time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        result_item.append(data)
    return result_item, pg


# 根据id获取日志
def log_get(id=None):
    result = RequestLog.query.get(id)
    return result


# 删除日志,根据请求id
def log_delete_db(id=None):
    try:
        log = log_get(id)   # 先获取再删除
        db.session.delete(log)
        db.session.commit()
        return True
    except Exception as e:
        return False
