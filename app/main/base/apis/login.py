# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.models import Users
from flask_security import login_user
from flask import session, request

from app.main.base import control

# import redis


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('id')


class LoginManage(Resource):

    def post(self):
        """
        登录
        ---
        tags:
          - login
        parameters:
          - in: formData
            name: username
            type: string
            required: true
          - in: formData
            name: password
            type: string
            required: true
        responses:
          200:
            description: 用户登录
            schema:
              id: User
              properties:
                id:
                  type: string
                  description: 用户id
                  default: Steven Wilson
                  name: code
        """
        args = parser.parse_args()
        try:
            if not all([args['username'], args['password']]):
                raise Exception('Incorrect username or password.')

            user = control.user.list_by_name(username=args['username'])

            if not user:
                raise Exception('Incorrect username or password.')
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
                    control.user.update_login_time(user)
        except Exception as e:
            return set_return_val(False, {}, str(e), 1301), 400
        return set_return_val(True, data, 'login successful', 1300)


