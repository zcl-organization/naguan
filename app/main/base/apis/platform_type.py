# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from auth import basic_auth
from app.common.tool import set_return_val
from app.main.base import control
from flask import g

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')


class PlatformTypeMg(Resource):

    @basic_auth.login_required
    def get(self):
        """
        查询云平台类型信息
        ---
       tags:
          - cloud platform type
       security:
       - basicAuth:
          type: http
          scheme: basic
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
        g.error_code = 1061
        try:

            data = control.platform_type.type_list(id=args['id'], name=args['name'])
        except Exception, e:
            return set_return_val(False, [], str(e), g.error_code), 400

        g.error_code = 1060
        return set_return_val(True, data, 'Platform type query succeeded.', g.error_code)

    @basic_auth.login_required
    def post(self):
        """
        创建平台类型
       ---
       tags:
          - cloud platform type
       security:
       - basicAuth:
          type: http
          scheme: basic
       produces:
          - "application/json"
       parameters:
         - in: body
           name: body
           required: true
           schema:
              required:
              - name
              properties:
                name:
                  type: string
                  default: vcenter
                  description: 平台类型名称
                  example: vCenter
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
        g.error_code = 1071
        try:
            if not args['name']:
                g.error_code = 1072
                raise Exception('Please pass in the platform type name.')

            platform_type = control.platform_type.type_create(name=args['name'])

        except Exception as e:
            control.event_logs.eventlog_create(type='platform_type', result=False, resources_id=None,
                                               event=unicode('增加平台类型'), submitter=g.username)
            return set_return_val(False, [], str(e), g.error_code), 400

        g.error_code = 1070
        control.event_logs.eventlog_create(type='platform_type', result=True, resources_id=platform_type[0]['id'],
                                           event=unicode('增加平台类型'), submitter=g.username)
        return set_return_val(True, [], 'Platform type create succeeded.', g.error_code)

    @basic_auth.login_required
    def put(self, id):
        """
        根据id更新云平台类型信息
       ---
       tags:
          - cloud platform type
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
        g.error_code = 1081  # TODO
        try:
            if not args['name']:
                g.error_code = 1082
                raise Exception('Please pass in the platform type name.')
            control.platform_type.type_update(id, args['name'])

        except Exception, e:
            control.event_logs.eventlog_create(type='platform_type', result=False, resources_id=id,
                                               event=unicode('更新平台类型信息'), submitter=g.username)
            return set_return_val(False, [], str(e), g.error_code), 400
            
        g.error_code = 1080
        control.event_logs.eventlog_create(type='platform_type', result=True, resources_id=id,
                                           event=unicode('更新平台类型信息'),
                                           submitter=g.username)
        return set_return_val(True, [], 'Platform type update succeeded.', g.error_code)

    @basic_auth.login_required
    def delete(self, id):
        """
        根据id删除云平台类型信息
       ---
       tags:
          - cloud platform type
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
            g.error_code = 1091
            control.platform_type.type_delete(id)
        except Exception as e:
            control.event_logs.eventlog_create(type='platform_type', result=False, resources_id=id,
                                               event=unicode('删除平台类型信息'), submitter=g.username)

            return set_return_val(False, [], str(e), g.error_code), 400
        
        g.error_code = 1090
        control.event_logs.eventlog_create(type='platform_type', result=True, resources_id=id,
                                           event=unicode('删除平台类型信息'),
                                           submitter=g.username)
        return set_return_val(True, [], 'Platform type delete succeeded.', g.error_code)
