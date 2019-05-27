# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.models import Users
from flask_security import login_user
from flask import session, request

from app.main.base import control
from app.code import Code

# import redis


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
            print(args['username'])
            if not all([args['username'], args['password']]):
                raise Exception('Incorrect username or password.')

            user = control.user.list_by_name(username=args['username'])

            if not user:
                # raise Exception('Incorrect username or password.')
                raise Exception('LoginParameterErr')
            else:
                if not user.verify_password(args['password']):
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
                    session[token] = True
                    # session['100'] = 1
                    # print(session.get(token))
                    control.user.update_login_time(user)
        except Exception as e:
            # print(Code(e))
            return set_return_val(False, {}, str(e), 1301), 400
        return set_return_val(True, data, 'login successful', 1300)
