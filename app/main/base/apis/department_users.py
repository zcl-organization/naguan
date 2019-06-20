# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import g
from app import set_return_val
from app.main.base import control
from auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('department_id')
parser.add_argument('department_name')
parser.add_argument('user_id')


class DepartmentUsersManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
        获取部门用户信息
        ---
       tags:
           - department user
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: department_id
            type: string
          - in: query
            name: user_id
            type: string
       responses:
          200:
            description: 获取部门信息
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
                      department_id:
                        type: string
                        default: 1
                        description: 部门编号
                        example: 1
                      department_user_id:
                        type: string
                        default: 1
                        description: 部门用户编号
                        example: 1
                      user_id:
                        type: string
                        default: 1
                        description: 用户编号
                        example: 1
                      user_name:
                        type: string
                        default: zcl
                        description: 用户名称
                        example: zcl
        """
        args = parser.parse_args()

        try:
            department = control.department_users.get_department_users(department_id=args['department_id'],
                                                                       user_id=args['user_id'])
        except Exception as e:
            return set_return_val(False, [], str(e), 400), 400
        # finally:
        #     control.event_logs.eventlog_create(**data)
        return set_return_val(True, department, 'get department user successfully', 1200)

    @basic_auth.login_required
    def post(self):
        """
        提交部门信息
        ---
       tags:
           - department user
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
              - company_name
              - company_mobile
              properties:
                department_id:
                  type: string
                  default: 1
                  description: 部门编号
                  example: 1
                user_id:
                  type: string
                  default: [1,2]
                  description: 用户编号
                  example: [1,2]
       responses:
          200:
            description: 提交单位信息
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
                      company_id:
                        type: string
                        default: 1
                        description: 单位编号
                        example: 1
                      department_id:
                        type: string
                        default: 1
                        description: 部门编号
                        example: 1
                      department_name:
                        type: string
                        default: 研三
                        description: 部门名称
                        example: 研三
                      department_pid:
                        type: string
                        default: 2
                        description: 上级部门编号
                        example: 2
        """
        data = dict(
            type='department',
            result=True,
            resources_id=None,
            event=unicode('添加部门用户信息'),
            submitter=g.username,
        )
        args = parser.parse_args()
        try:
            if not all([args['department_id'], args['user_id']]):
                raise Exception('Parameter error')
            department_user = control.department_users.update_department_users(department_id=args['department_id'],
                                                                               user_id=args['user_id'])
            # data['resources_id'] = department[0]['department_id']
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, department_user, 'create department user successfully', 1200)

    @basic_auth.login_required
    def put(self, department_id):
        """
        更新部门用户信息
        ---
       tags:
           - department user
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: department_id
           type: integer
           format: int64
           required: true
         - in: formData
           name: user_id
           type: string
       responses:
         200:
            description: 更新单位信息
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
        data = dict(
            type='department',
            result=True,
            resources_id=None,
            event=unicode('添加部门用户信息'),
            submitter=g.username,
        )
        try:
            if not all([department_id, args['user_id']]):
                raise Exception('Parameter error')
            control.department_users.update_department_users(department_id=department_id,
                                                             user_id=args['user_id'])
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 1220)
        finally:
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'update department user successfully', 1220)

    @basic_auth.login_required
    def delete(self, department_id):
        """
        清除部门用户信息
        ---
       tags:
          - department user
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: department_id
           type: integer
           format: int64
           required: true
       responses:
         200:
            description: 删除部门信息
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
            if not department_id:
                raise Exception('Parameter error')
            control.department_users.delete_department_user(department_id=department_id)
        except Exception as e:
            return set_return_val(False, [], str(e), 2451), 400
        return set_return_val(True, [], 'delete role menu successfully', 1220)
