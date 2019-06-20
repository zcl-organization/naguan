# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import g
from app import set_return_val
from app.main.base import control
from auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('department_id')
parser.add_argument('department_name')
parser.add_argument('department_remarks')
parser.add_argument('department_status')
parser.add_argument('department_pid')
parser.add_argument('company_id')
parser.add_argument('company_name')


# parser.add_argument('pid')


class DepartmentManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
        获取部门信息
        ---
       tags:
           - department
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: department_id
            type: string
          - in: query
            name: department_name
            type: string
          - in: query
            name: company_name
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
                      company_id:
                        type: string
                        default: company_id
                        description: 单位编号
                        example: 1
                      company_name:
                        type: string
                        default: company_name
                        description: 单位名称
                        example: 什么马科技
                      department_id:
                        type: string
                        default: 1
                        description: 部门编号
                        example: 1
                      department_name:
                        type: string
                        default: company_fax
                        description: 部门名称
                        example: 研三
                      department_pid:
                        type: string
                        default: department_pid
                        description: 上级部门编号
                        example: 1
                      department_remarks:
                        type: string
                        default: 1
                        description: 备注
                        example: 1
                      department_status:
                        type: string
                        default: 1
                        description: 部门状态
                        example: 1
        """
        data = dict(
            type='department',
            result=True,
            resources_id=None,
            event=unicode('获取部门信息'),
            submitter=g.username,
        )
        args = parser.parse_args()

        try:
            department = control.department.get_department(department_id=args['department_id'],
                                                           department_name=args['department_name'],
                                                           company_name=args['company_name'])
            # data['resources_id'] = department[0]['department_id']
        except Exception as e:
            # data['result'] = False
            return set_return_val(False, [], str(e), 400), 400
        # finally:
        #     control.event_logs.eventlog_create(**data)
        return set_return_val(True, department, 'Create department successfully', 1200)

    @basic_auth.login_required
    def post(self):
        """
        提交部门信息
        ---
       tags:
           - department
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
                department_name:
                  type: string
                  default: 研三
                  description: 部门名称
                  example: 研三
                department_remarks:
                  type: string
                  default: 备注
                  description: 备注
                  example: 备注哟
                company_id:
                  type: string
                  default: 1
                  description: 单位编号
                  example: 1
                department_pid:
                  type: string
                  default: 1
                  description: 上级部门编号
                  example: 1
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
            event=unicode('添加部门信息'),
            submitter=g.username,
        )
        args = parser.parse_args()
        try:
            if not all([args['department_name'], args['company_id']]):
                raise Exception('Parameter error')
            department = control.department.create_department(department_name=args['department_name'],
                                                              department_remarks=args['department_remarks'],
                                                              company_id=args['company_id'],
                                                              department_pid=args['department_pid'])
            # data['resources_id'] = department[0]['department_id']
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, department, 'Create department successfully', 1200)

    @basic_auth.login_required
    def put(self, department_id):
        """
        更新部门信息
        ---
       tags:
           - department
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
           name: department_name
           type: string
         - name: department_remarks
           type: string
           in: formData
         - name: department_status
           type: string
           in: formData
         - name: department_pid
           type: string
           in: formData
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
        data = dict(
            type='department',
            result=False,
            resources_id=None,
            event=unicode('更新部门信息'),
            submitter=g.username
        )
        try:
            args = parser.parse_args()
            if not department_id:
                g.error_code = 5000
                raise Exception('Parameter error')
            control.department.update_department_by_id(department_id=department_id,
                                                       department_name=args['department_name'],
                                                       department_remarks=args['department_remarks'],
                                                       department_status=args['department_status'],
                                                       department_pid=args['department_pid'])
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = department_id
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'department update success.', 2020)

    @basic_auth.login_required
    def delete(self, department_id):
        """
        删除部门信息
        ---
       tags:
          - department
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
        data = dict(
            type='department',
            result=False,
            resources_id=None,
            event=unicode('删除单位信息'),
            submitter=g.username
        )
        try:
            if not department_id:
                g.error_code = 5000
                raise Exception('Parameter error')
            control.department.delete_department_by_id(department_id)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = department_id
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'department delete success.', 2020)
