# -*- coding:utf-8 -*-

from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app, db
from flask import g, request, current_app
from app.models import RequestLog

import json
import os
import datetime
import uuid

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.before_first_request
def first_request():
    with open('policy.json', 'r') as f:
        json_dict = json.load(f)
    # print(g.policy)
    app.config['POLICY'] = json_dict


@app.before_request
def before_request_info():
    base_url = request.base_url
    method = request.method
    g.ip = request.remote_addr
    g.url = method + '/' + base_url
    g.time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    g.username = ''

    g.request_id = str(uuid.uuid5(uuid.uuid4(), 'kaopuyun'))

    g.log_d = {
        'ip': g.ip,
        'url': g.url,
        'time': g.time,
        'username': g.username,
        'request_id': g.request_id,
    }


@app.after_request
def teardown_request(res):
    try:
        request_log = RequestLog()
        request_log.request_id = g.request_id
        request_log.ip = g.ip
        request_log.url = g.url
        request_log.time = g.time
        request_log.submitter = g.username
        request_log.status_num = res.status_code
        g.log_d['status_code'] = res.status_code
        current_app.logger.info(g.log_d)
        db.session.add(request_log)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
    return res


# @app.after_request
# def after_request():
#     print(g.username)
#

# def

#
# @app.before_request
# @httpauth.login_required
# def check_policy():
#     # 从config中获取policy
#     print('check_policy')
#     g.policy = app.config['POLICY']
#     if request.path.count('/') == 1:
#         endpoint = request.path.strip('/')
#     else:
#         url_list = request.path.split('/')
#         if url_list[0]:
#             endpoint = ':'.join(url_list)
#         else:
#             del url_list[0]
#             endpoint = ':'.join(url_list)
#
#     # 判断权限
#     if endpoint in g.policy:
#         policy = g.policy[endpoint]
#         if policy:
#             if '_or_' in policy:
#                 need_policy_list = policy.split(':')[1].split('_or_')
#             else:
#                 need_policy_list = [policy.split(':')[1]]
#
#             print(need_policy_list)
#         else:
#             need_policy_list = []
#         # print(dir(current_user))
#         if need_policy_list:
#             for policy_tmp in need_policy_list:
#                 if current_user.has_role(policy_tmp):
#                     policy_flag = True
#                     break
#                 else:
#                     policy_flag = False
#             if not policy_flag:
#                 data = {
#                     'status': 0,
#                     'msg': '用户没有权限访问接口',
#                     'data': ''
#                 }
#                 return jsonify(data)
#
#     else:
#         print(endpoint, 'not in policy')


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
