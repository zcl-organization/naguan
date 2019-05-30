# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

from auth import basic_auth
from app.common.tool import set_return_val
from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('role_id')
parser.add_argument('new_role_id')
parser.add_argument('old_role_id')

parser.add_argument('role_name', type=str)
parser.add_argument('user_name', type=str)


class RolesUsersManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取用户角色列表
         ---
       tags:
           - user_role
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: query
           type: string
           name: user_name
           description: 用户名
         - in: query
           name: role_name
           type: string
           description: 角色名
       responses:
           200:
            description: 获取用户角色信息
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
                      role_id:
                        type: string
                        default: 1
                        description: role_id
                      role_name:
                        type: string
                        default: admin
                        description: role_name
                      user_id:
                        type: string
                        default: 1
                        description: user_id
                      user_name:
                        type: string
                        default: admin
                        description: user_name
         """
        try:

            args = parser.parse_args()
            # user_name = args.get('user_name')
            # role_name = args.get('role_name')
            # 获取所有用户角色权限 列表
            # data = role_user_manage.role_user_list(args['user_name'], args['role_name'])
            data = control.roles_users.role_user_list(args['user_name'], args['role_name'])
        except Exception as e:
            return set_return_val(False, {}, str(e), 1234), 400
        return set_return_val(True, data, '获取列表成功', 1234)

    @basic_auth.login_required
    def post(self):
        """
         用户角色分配
         ---
       tags:
           - user_role
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
               - user_id
               - role_id
               properties:
                 user_id:
                   type: integer
                   default: 1
                   description: 用户id
                   example: 1
                 role_id:
                   type: integer
                   default: 1
                   description: 角色id
                   example: 1
       responses:
           200:
            description: 用户角色分配
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
            user_id = args.get('user_id')
            role_id = args.get('role_id')
            # if user_id and role_id:
            if not all([user_id, role_id]):
                raise Exception('参数错误,参数不能为空')

            user_username, role_name = control.roles_users.role_user_add(user_id, role_id)
        except Exception as e:
            control.event_logs.eventlog_create(type='roles_users', result=False, resources_id='',
                                               event=unicode('为用户分配角色'), submitter=g.username)
            return set_return_val(False, {}, str(e), 1234), 400
        control.event_logs.eventlog_create(type='roles_users', result=True, resources_id='',
                                           event=unicode('为用户:%s 分配角色:%s' % (user_username, role_name)),
                                           submitter=g.username)
        return set_return_val(True, {}, '用户角色添加成功', 1234)

    @basic_auth.login_required
    def put(self):
        """
         用户角色更新
         ---
       tags:
           - user_role
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
           - in: query
             type: string
             name: user_id
             description: 用户id
           - in: query
             name: new_role_id
             type: string
             description: 新角色id
           - in: query
             name: old_role_id
             type: string
             description: 旧角色id
       responses:
           200:
            description: 用户角色重新分配
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
        # 更新用户角色
        try:
            args = parser.parse_args()
            user_id = args.get('user_id')
            new_role_id = args.get('new_role_id')
            old_role_id = args.get('old_role_id')

            if not all([user_id, new_role_id, old_role_id]):
                raise Exception('参数错误,参数不能为空')

            username, new_name, old_name = control.roles_users.role_user_update(user_id, new_role_id, old_role_id)
        except Exception as e:
            control.event_logs.eventlog_create(type='roles_users', result=False, resources_id='',
                                               event=unicode('更新用户角色'), submitter=g.username)
            return set_return_val(False, {}, str(e), 1234), 400

        control.event_logs.eventlog_create(type='roles_users', result=True, resources_id=user_id,
                                           event=unicode('更新用户:%s 的角色 %s 为  %s' % (username, old_name, new_name))
                                           , submitter=g.username, role_id=new_role_id)
        return set_return_val(True, {}, '用户角色更新成功', 1234)

    @basic_auth.login_required
    def delete(self):
        """
         用户角色删除
         ---
       tags:
           - user_role
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
           - in: query
             type: string
             name: user_id
             description: 用户id
       responses:
           200:
            description: 删除用户角色
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
        # 删除用户所有角色
        try:
            args = parser.parse_args()
            user_id = args.get('user_id')
            if not user_id:
                raise Exception('参数错误,参数不能为空')
            username = control.roles_users.role_user_delete(user_id)
        except Exception as e:
            control.event_logs.eventlog_create(type='roles_users', result=False, resources_id='',
                                               event=unicode('删除用户角色'), submitter=g.username)
            return set_return_val(False, {}, str(e), 1234), 400
        control.event_logs.eventlog_create(type='roles_users', result=True, resources_id='',
                                           event=unicode('删除用户:%s 的角色' % username),
                                           submitter=g.username, user_id=user_id)
        return set_return_val(True, {}, '用户角色删除成功', 1234)
