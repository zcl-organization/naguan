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
parser.add_argument('company_id')
parser.add_argument('company_name')
parser.add_argument('pid')


class DepartmentManage(Resource):
    def get(self):
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

    def post(self):
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
                                                              company_id=args['company_id'], pid=args['pid'])
            data['resources_id'] = department[0]['department_id']
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 404), 400
        finally:
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, department, 'Create department successfully', 1200)

    def put(self, department_id):
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

    def delete(self, department_id):
        data = dict(
            type='department',
            result=False,
            resources_id=None,
            event=unicode('删除单位信息'),
            submitter=g.username
        )
        try:
            if not department_id:
                raise Exception('Parameter error')
            control.department.delete_department_by_id(department_id)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = department_id
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'department delete success.', 2020)
