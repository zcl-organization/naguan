# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from auth import basic_auth
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
parser.add_argument('name')


class UserManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
        获取用户信息
        ---
       tags:
          - user
       security:
       - basicAuth:
          type: http
          scheme: basic
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
          - name: name
            type: string
            in: query
            description: 用户名称
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
            description: 获取用户信息
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
                pg:
                  type: array
                  items:
                    properties:
                      has_next:
                        type: boolean
                        default: kpy
                        description: has_next
                      has_prev:
                        type: boolean
                        default: kpy
                        description: has_prev
                      page:
                        type: string
                        default: kpy
                        description: page
                      pages:
                        type: string
                        default: kpy
                        description: pages
                      size:
                        type: string
                        default: kpy
                        description: size
                      total:
                        type: string
                        default: kpy
                        description: total
                data:
                  type: array
                  items:
                    properties:
                      company:
                        type: string
                        default: kpy
                        description: 公司
                      current_login_ip:
                        type: string
                        default: kpy
                        description: current_login_ip
                      date_created:
                        type: string
                        default: kpy
                        description: date_created
                      department:
                        type: string
                        default: kpy
                        description: department
                      email:
                        type: string
                        default: kpy
                        description: email
                      first_name:
                        type: string
                        default: kpy
                        description: first_name
                      id:
                        type: string
                        default: kpy
                        description: id
                      job:
                        type: string
                        default: kpy
                        description: job
                      last_login_at:
                        type: string
                        default: kpy
                        description: last_login_at
                      last_login_ip:
                        type: string
                        default: kpy
                        description: last_login_ip
                      location:
                        type: string
                        default: kpy
                        description: location
                      login_count:
                        type: string
                        default: kpy
                        description: login_count
                      mobile:
                        type: string
                        default: kpy
                        description: mobile
                      name:
                        type: string
                        default: kpy
                        description: name
                      sex:
                        type: string
                        default: kpy
                        description: sex
                      uac:
                        type: string
                        default: kpy
                        description: uac
                      uid:
                        type: string
                        default: kpy
                        description: uid
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
                                              name=args['name'], remarks=args['remarks'], next_page=pgnum, limit=limit)
        except Exception as e:
            return set_return_val(True, [], 'Failed to get user information', 1101), 400

        return set_return_val(True, data, 'Successfully obtained user information', 1100, pg)

    # @basic_auth.login_required
    def post(self):
        """
       新增用户信息
       ---
       tags:
          - user
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: body
           name: body
           required: true
           schema:
             required:
             - username
             - password
             - email
             - first_name
             - uid
             - mobile
             - department
             - company
             - sex
             properties:
               username:
                 type: string
                 default: test
                 description: 用户名
                 example: test
               password:
                 type: string
                 default: aaaaaa
                 description: 密码
                 example: aaaaaa
               email:
                 type: string
                 default: test@qq.com
                 description: email
                 example: test@qq.com
               first_name:
                 type: string
                 default: test
                 description: first_name
                 example: test
               uid:
                 type: integer
                 default: 1
                 description: uid
                 example: 1
               mobile:
                 type: string
                 default: 15060011111
                 description: mobile
                 example: 15060011111
               department:
                 type: string
                 default: 研三
                 description: 部门
                 example: 研三
               company:
                 type: string
                 default: kpy
                 description: 公司名称
                 example: kpy
               sex:
                 type: integer
                 default: 1
                 description: 性别
                 example: 1
               remarks:
                 type: integer
                 default: 备注
                 description: 备注
                 example: 备注

       responses:
         200:
            description: 添加用户信息
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
            if not args['sex']:
                sex = 1
            else:
                sex = args['sex']

            user = control.user.user_create(username=args['username'], password=args['password'], email=args['email'],
                                            first_name=args['first_name'], uid=1, mobile=args['mobile'],
                                            department=args['department'], job='it', location='location',
                                            company=args['company'], sex=int(sex), uac='uac', active=active,
                                            is_superuser=is_superuser, remarks=args['remarks'], current_login_ip=g.ip)


        # 已存在
        except ExistsException as e:
            control.event_logs.eventlog_create(type='user', result=False, resources_id='',
                                               event=unicode('创建新用户：已存在'), submitter=g.username)
            return set_return_val(False, [], str(e), 1002), 400

        except Exception as e:
            control.event_logs.eventlog_create(type='user', result=False, resources_id='',
                                               event=unicode('创建新用户'), submitter=g.username)
            return set_return_val(False, [], str(e), 1001), 400
        control.event_logs.eventlog_create(type='user', result=True, resources_id=user[0]['id'],
                                           event=unicode('创建新用户:%s' % args['username']), submitter=g.username)
        return set_return_val(True, user, 'User created successfully', 1000)

    @basic_auth.login_required
    def put(self, id):
        """
        更新用户信息
        ---
       tags:
          - user
       security:
       - basicAuth:
          type: http
          scheme: basic
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
            description: 更新用户信息
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
        """

        args = parser.parse_args()

        # 验证 active 合法性
        if args['active']:
            if int(args['active']) not in [1, 2]:
                return set_return_val(False, [], str('Please pass in the correct parameters. 1 is True and 2 is False'),
                                      1001), 400
        # if args['active'] or args['password']:
        #     pass
        # else:
        #     return set_return_val(False, [], str('Please pass in the field that needs to be modified'),
        #                           1001), 400
        try:

            username = control.user.user_update(id=id, active=args['active'], username=args['username'],
                                                password=args['password'], mobile=args['mobile'],
                                                company=args['company'],
                                                department=args['department'], remarks=args['remarks'])

        except Exception, e:
            control.event_logs.eventlog_create(type='user', result=False, resources_id=id,
                                               event=unicode('更新用户'), submitter=g.username)
            return set_return_val(False, [], str(e), 1001), 400
        control.event_logs.eventlog_create(type='user', result=True, resources_id=id,
                                           event=unicode('更新用户:%s' % username), submitter=g.username)
        return set_return_val(True, [], 'User update successfully', 3000)

    @basic_auth.login_required
    def delete(self, id):
        """
        根据id用户信息
       ---
       tags:
          - user
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
            description: 删除用户信息
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
        """
        try:
            username = control.user.user_delete(id=id)

        except Exception, e:
            control.event_logs.eventlog_create(type='user', result=True, resources_id=id,
                                               event=unicode('删除用户'), submitter=g.username)
            return set_return_val(False, [], str(e), 1001), 400
        control.event_logs.eventlog_create(type='user', result=True, resources_id=id,
                                           event=unicode('删除用户:%s' % username), submitter=g.username)
        return set_return_val(True, [], 'User delete successfully', 3000)
