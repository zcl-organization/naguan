# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.models import Users
from flask_security import login_user
from flask import session, request

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
            users = Users.query.filter_by(username=args['username']).first()
            # print('status:', users.verify_password(args['password']))
            # if not users or not users.verify_password(args['password']):
            if not users:
                raise Exception('Incorrect username or password.')
            else:
                if not users.verify_password(args['password']):
                    raise Exception('Incorrect username or password.')
                else:
                    login_user(users, True)
                    token = users.generate_auth_token()
                    # token = create_token(users.id, users.username)
                    data = {
                        'token': token,
                        'id': users.id,
                        'username': users.username,
                        'email': users.email,
                        'mobile': users.mobile,
                        'department': users.department,
                        'job': users.job,
                        'location': users.location,
                        'sex': users.sex,
                        'remarks': users.remarks
                    }
                    session[token] = True
        except Exception as e:
            return set_return_val(False, {}, str(e), 1301), 400
        return set_return_val(True, data, 'login successful', 1300)

    def get(self):
        print('debug:', request.args.get('debug'))
        print('get')
        return 'ccc'
