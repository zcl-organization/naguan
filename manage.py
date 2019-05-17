# -*- coding:utf-8 -*-

from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from app import create_app, db
from flask import g, request, current_app
from app.models import RequestLog

import json
import os
import datetime
import uuid

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.before_first_request
def before_first_request():
    with open('policy.json', 'r') as f:
        json_dict = json.load(f)
    # print(g.policy)
    app.config['POLICY'] = json_dict


@app.before_request
def before_request():
    base_url = request.base_url
    method = request.method
    g.ip = request.remote_addr
    g.url = method + '/' + base_url
    g.time = datetime.datetime.now()
    g.username = 'anonymous'

    g.request_id = str(uuid.uuid5(uuid.uuid4(), 'kaopuyun'))

    g.log_d = {
        'ip': g.ip,
        'url': g.url,
        'time': g.time,
        'username': g.username,
        'request_id': g.request_id,
    }


@app.after_request
def after_request(res):
    try:
        request_log = RequestLog()
        request_log.request_id = g.request_id
        request_log.ip = g.ip
        request_log.url = g.url
        request_log.time = g.time
        request_log.submitter = g.username
        request_log.status_num = res.status_code
        g.log_d['status_code'] = res.status_code
        # current_app.logger.info(g.log_d)
        db.session.add(request_log)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
    return res


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()
#     if exception and db.session.is_active:
#         db.session.rollback()


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(
    host='0.0.0.0', port='5000', threaded=True))

if __name__ == '__main__':
    manager.run()
