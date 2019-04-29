# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.my_exceptions import ExistsException
from app.common.tool import set_return_val
from app.main.base import control
from flask import g

# from sqlalchemy.exc import DBAPIError

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('email')
parser.add_argument('first_name')
parser.add_argument('uid')
parser.add_argument('mobile')
parser.add_argument('department')
parser.add_argument('job')
parser.add_argument('location')
parser.add_argument('company')
parser.add_argument('sex')
parser.add_argument('uac')
parser.add_argument('active')
parser.add_argument('is_superuser')
parser.add_argument('remarks')
parser.add_argument('last_login_ip')
parser.add_argument('current_login_ip')
parser.add_argument('pgnum')
parser.add_argument('pgsize')


class UserManage(Resource):

    def get(self):
        """
        获取用户信息
        ---
        tags:
          - user
        summary: Add a new pet to the store
        parameters:
          - in: query
            name: id
            type: string
            description: 用户id
          - name: email
            type: string
            in: query
            description: 邮箱
          - name: mobile
            type: string
            in: query
            description: 手机号码
          - name: remarks
            type: string
            in: query
            description: 备注
          - in: query
            name: pgnum
            type: string
            description: 页码
          - in: query
            name: pgsize
            type: string
            description: 单页显示个数
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """

        args = parser.parse_args()

        if not args['pgnum']:
            pgnum = 1
        else:
            pgnum = int(args['pgnum'])
        if not args['pgsize']:
            limit = 10
        else:
            limit = int(args['pgsize'])

        try:
            data, pg = control.user.user_list(user_id=args['id'], email=args['email'], mobile=args['mobile'],
                                              remarks=args['remarks'], next_page=pgnum, limit=limit)
        except Exception as e:
            return set_return_val(True, [], 'Failed to get user information', 1101), 400
        return set_return_val(True, data, 'Successfully obtained user information', 1100, pg)

    def post(self):
        """
       新增用户信息
       ---
       tags:
          - user
       parameters:
         - in: formData
           name: username
           type: string
           required: true
         - in: formData
           name: password
           type: string
           required: true
         - in: formData
           name: email
           type: string
           required: true
         - in: formData
           name: first_name
           type: string
           required: true
         - in: formData
           name: uid
           type: string
           required: true
         - in: formData
           name: mobile
           type: string
           required: true
         - in: formData
           name: department
           type: string
           required: true
         - in: formData
           name: company
           type: string
           required: true
         - in: formData
           name: sex
           type: integer
           format: int64
           required: true
         - in: formData
           name: remarks
           type: string
       responses:
         200:
           description: A single user create item
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """
        try:
            args = parser.parse_args()
            parser.add_argument('username')
            parser.add_argument('password')
            parser.add_argument('email')

            if not all([args['username'], args['password'], args['email'], args['department'], args['company']]):
                return set_return_val(False, [], str('Parameter error.'), 1002), 400

            active = 1
            is_superuser = 1

            control.user.user_create(username=args['username'], password=args['password'], email=args['email'],
                                     first_name=args['first_name'], uid=1, mobile=args['mobile'],
                                     department=args['department'], job='it', location='location',
                                     company=args['company'], sex=int(args['sex']), uac='uac', active=active,
                                     is_superuser=is_superuser, remarks=args['remarks'], current_login_ip=g.ip)

        # 已存在
        except ExistsException as e:
            return set_return_val(False, [], str(e), 1002), 400

        except Exception as e:
            return set_return_val(False, [], str(e), 1001), 400

        return set_return_val(True, [], 'User created successfully', 1000)

    def put(self, id):
        """
        更新用户信息
        ---
        tags:
          - user
        parameters:
         - in: path
           type: integer
           format: int64
           name: id
           required: true
         - in: query
           name: username
           type: string
         - in: query
           name: active
           type: string
         - name: password
           type: string
           in: query
         - name: mobile
           type: string
           in: query
         - name: company
           type: string
           in: query
         - name: department
           type: string
           in: query
         - name: remarks
           type: string
           in: query
        responses:
         200:
           description: 更新用户名和状态
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """

        args = parser.parse_args()

        # 验证 active 合法性
        if args['active']:
            if int(args['active']) not in [1, 2]:
                return set_return_val(False, [], str('Please pass in the correct parameters. 1 is True and 2 is False'),
                                      1001), 400
        if args['active'] or args['password']:
            pass
        else:
            return set_return_val(False, [], str('Please pass in the field that needs to be modified'),
                                  1001), 400
        try:

            control.user.user_update(id=id, active=int(args['active']), username=args['username'],
                                     password=args['password'], mobile=args['mobile'], company=args['company'],
                                     department=args['department'], remarks=args['remarks'])

        except Exception, e:

            return set_return_val(False, [], str(e), 1001), 400
        return set_return_val(True, [], 'User update successfully', 3000)

    def delete(self, id):
        """
        根据id用户信息
       ---
       tags:
          - user
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
           description: 根据用户id删除用户信息
           schema:
             id: User
             properties:
               id:
                 type: string
                 description: 用户id
                 default: Steven Wilson
        """
        try:
            control.user.user_delete(id=id)

        except Exception, e:
            return set_return_val(False, [], str(e), 1001), 400

        return set_return_val(True, [], 'User delete successfully', 3000)
