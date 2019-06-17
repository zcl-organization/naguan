# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from flask_security import login_user
from flask import session, g

from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('id')
parser.add_argument('body')


class LoginManage(Resource):

    def post(self):
        """
        登录
        ---
        tags:
          - login
        produces:
          - "application/json"
        parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
              - username
              - password
              properties:
                username:
                  type: string
                  default: zcl
                  description: 用户名
                  required: True
                password:
                  type: string
                  default: zcl
                  description: 密码
        responses:
          200:
            description: 用户登录
            schema:
             properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      department:
                        type: string
                        default: 研发三部
                      email:
                        type: string
                        default: 843050672@qq.com
                      id:
                        type: int
                        default: 1
                      job:
                        type: string
                        default: it
                      location:
                        type: string
                        default: location
                      mobile:
                        type: string
                        default: 15060011111
                      remarks:
                        type: string
                        default: remarks
                      sex:
                        type: int
                        default: 1
                      token:
                        type: string
                        default: eyJhbGciOiJIUzU3rKdzH6FW4HohJ32LQqnQ1sLzVqXiuArh8Nco3KJpA_CsLlxwM9-EZe5P_XF8I4US9WN6Q
                      username:
                        type: string
                        default: kpy
        """
        args = parser.parse_args()
        try:
            if not all([args['username'], args['password']]):
                g.error_code = 1001
                raise Exception('Incorrect username or password.')

            user = control.user.list_by_name(username=args['username'])

            if not user:
                g.error_code = 1002
                raise Exception('Incorrect username or password.')

            else:
                if not user.verify_password(args['password']):
                    g.error_code = 1003
                    raise Exception('Incorrect username or password.')
                else:
                    login_user(user, True)
                    token = user.generate_auth_token()
                    # token = create_token(users.id, users.username)
                    data = {
                        'token': token,
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'mobile': user.mobile,
                        'department': user.department,
                        'job': user.job,
                        'location': user.location,
                        'sex': user.sex,
                        'remarks': user.remarks
                    }
                    # session['username'] = user.username
                    g.username = user.username
                    session[token] = True
                    control.user.update_login_time(user)
        except Exception as e:

            control.event_logs.eventlog_create(type='login', result=False, resources_id=None, event=unicode('登陆'),
                                               submitter=args['username'])

            return set_return_val(False, {}, str(e), g.error_code), 400

        control.event_logs.eventlog_create(type='login', result=True, resources_id=user.id, event=unicode('登陆'),
                                           submitter=g.username)
        return set_return_val(True, data, 'login successful', 1000)
