# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import g
from app import set_return_val
from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('department_id')
parser.add_argument('department_name')
parser.add_argument('user_id')


class DepartmentUsersManage(Resource):
    def get(self):
        args = parser.parse_args()

        try:
            department = control.department_users.get_department_users(department_id=args['department_id'],
                                                                       user_id=args['user_id'])
        except Exception as e:
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
            if not all([args['department_id'], args['user_id']]):
                raise Exception('Parameter error')
            department = control.department_users.update_department_users(department_id=args['department_id'],
                                                                          user_id=args['user_id'])
            data['resources_id'] = department[0]['department_id']
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 404), 400
        finally:
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, department, 'Create department successfully', 1200)

    def put(self, department_id):
        args = parser.parse_args()
        if not all([department_id, args['user_id']]):
            raise Exception('Parameter error')
        try:
            department = control.department_users.update_department_users(department_id=department_id,
                                                                          user_id=args['user_id'])
        except Exception as e:
            return set_return_val(False, [], 'update role menu failed', 1220)
        return set_return_val(True, [], 'update role menu successfully', 1220)

    def delete(self, department_id):
        try:
            control.department_users.delete_department_user(department_id=department_id)
        except Exception as e:
            return set_return_val(False, [], str(e), 2451), 400
        return set_return_val(True, [], 'delete role menu successfully', 1220)
