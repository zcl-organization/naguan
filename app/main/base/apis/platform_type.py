# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from auth import basic_auth
from app.common.tool import set_return_val
from app.main.base import control
from flask import g

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')

ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': ''
}


class PlatformTypeMg(Resource):
    def get(self):
        """
        查询云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: query
           name: id
           type: integer
           format: int64
         - in: query
           name: name
           type: string
           description: 平台类型名称
       responses:
          200:
            description: 查询平台类型
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
                      id:
                        type: string
                        default: 1
                        description: id
                      name:
                        type: string
                        default: vcenter
                        description: 平台类型名称

        """
        args = parser.parse_args()
        try:

            data = control.platform_type.type_list(id=args['id'], name=args['name'])
        except Exception, e:
            return set_return_val(False, [], str(e), 1531), 400

        return set_return_val(True, data, 'Platform type query succeeded.', 1530)

    @basic_auth.login_required
    def post(self):
        """
        创建平台类型
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: query
           name: name
           type: string
           description: 平台类型名称
       responses:
         200:
            description: 创建平台类型
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

        if not args['name']:
            raise Exception('Please pass in the platform type name.')

        try:
            id = control.platform_type.type_create(name=args['name'])

        except Exception as e:
            control.event_logs.eventlog_create(type='platform_type', result=False, resources_id='',
                                               event=unicode('增加平台类型'), submitter=g.username)
            return set_return_val(False, [], str(e), 1501), 400
        control.event_logs.eventlog_create(type='platform_type', result=True, resources_id=id, event=unicode('增加平台类型'),
                                           submitter=g.username)
        return set_return_val(True, [], 'Platform type create succeeded.', 1500)

    @basic_auth.login_required
    def put(self, id):
        """
        根据id更新云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
         - in: query
           name: name
           type: string
           description: 平台类型名称
       responses:
         200:
            description: 更新平台类型
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
        if not args['name']:
            raise Exception('Please pass in the platform type name.')
        try:
            control.platform_type.type_update(id, args['name'])

        except Exception, e:
            control.event_logs.eventlog_create(type='platform_type', result=False, resources_id=id,
                                               event=unicode('更新平台类型信息'), submitter=g.username)
            return set_return_val(False, [], str(e), 1521), 400
        control.event_logs.eventlog_create(type='platform_type', result=True, resources_id=id, event=unicode('更新平台类型信息'),
                                           submitter=g.username)
        return set_return_val(True, [], 'Platform type update succeeded.', 1520)

    @basic_auth.login_required
    def delete(self, id):
        """
        根据id删除云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
            description: 删除平台类型
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
            control.platform_type.type_delete(id)
        except Exception as e:
            control.event_logs.eventlog_create(type='platform_type', result=False, resources_id=id,
                                               event=unicode('删除平台类型信息'), submitter=g.username)
            return set_return_val(False, [], str(e), 1511), 400
        control.event_logs.eventlog_create(type='platform_type', result=True, resources_id=id, event=unicode('删除平台类型信息'),
                                           submitter=g.username)
        return set_return_val(True, [], 'Platform type delete succeeded.', 1510)
