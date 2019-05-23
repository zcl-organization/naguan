# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

from auth import basic_auth
from app.common.tool import set_return_val
from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('platform_type_id')
parser.add_argument('platform_name')
parser.add_argument('ip')
parser.add_argument('port')
parser.add_argument('admin_name')
parser.add_argument('admin_password')
parser.add_argument('remarks')


class CloudPlatformManage(Resource):
    def get(self):
        """
        获取云平台信息
        ---
        tags:
          - cloudplatform
        parameters:
          - in: query
            name: id
            type: string
          - in: query
            name: platform_type_id
            type: string
          - in: query
            name: platform_name
            type: string
        responses:
          200:
            description: 获取平台信息
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
                        default: 200
                        description: id
                      ip:
                        type: string
                        default: 192.168.12.205
                        description: ip
                      name:
                        type: string
                        default: vcenter
                        description: name
                      password:
                        type: string
                        default: 123456
                        description: passwd
                      platform_name:
                        type: string
                        default: vcenter
                        description: platform_name
                      platform_type_id:
                        type: string
                        default: 1
                        description: platform_type_id
                      port:
                        type: string
                        default: 443
                        description: port
                      remarks:
                        type: string
                        default: ddddcv
                        description: remarks
        """
        args = parser.parse_args()
        try:
            data = control.cloud_platform.platform_list(id=args['id'],
                                                        platform_type_id=args['platform_type_id'],
                                                        platform_name=args['platform_name'])

        except Exception, e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'Platform list succeeded.', 1520)

    @basic_auth.login_required
    def post(self):
        """
       新增云平台信息
       ---
       tags:
          - cloudplatform
       parameters:
         - in: formData
           name: platform_type_id
           type: string
           required: true
         - in: formData
           name: platform_name
           type: string
           required: true
         - in: formData
           name: admin_name
           type: string
           required: true
         - in: formData
           name: admin_password
           type: string
           required: true
         - in: formData
           name: port
           type: string
           required: true
         - in: formData
           name: ip
           type: string
           required: true
         - in: formData
           name: remarks
           type: string
           required: true
       responses:
         200:
            description: 新增平台信息
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
        if not all([args['platform_type_id'], args['platform_name'], args['admin_name'], args['admin_password'],
                    args['ip']]):
            raise Exception('Parameter error')
        try:

            control.cloud_platform.platform_create(platform_type_id=args['platform_type_id'],
                                                   platform_name=args['platform_name'],
                                                   admin_name=args['admin_name'],
                                                   admin_password=args['admin_password'], port=args['port'],
                                                   ip=args['ip'], remarks=args['remarks'])

        except Exception, e:
            return set_return_val(False, [], str(e), 1501), 400
        control.event_logs.eventlog_create(type='cloud_platform', result=True, resources_id='', event=unicode('新增云平台信息')
                                           , submitter=g.username)
        return set_return_val(True, [], str('The platform information was created successfully.'), 1500)

    @basic_auth.login_required
    def put(self, id):
        """
        更新云平台信息
        ---
        tags:
          - cloudplatform
        parameters:
         - in: path
           type: integer
           format: int64
           name: id
           required: true
         - in: formData
           name: admin_name
           type: string
         - name: admin_password
           type: string
           in: formData
         - name: ip
           type: string
           in: formData
         - name: port
           type: string
           in: formData
         - name: remarks
           type: string
           in: formData
        responses:
         200:
            description: 更新平台信息
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
        try:
            control.cloud_platform.platform_update(id, ip=args['ip'], admin_name=args['admin_name'],
                                                   admin_password=args['admin_password'], port=args['port'],
                                                   remarks=args['remarks'])
        except Exception, e:
            return set_return_val(False, [], str(e), 1529), 400
        control.event_logs.eventlog_create(type='cloud_platform', result=True, resources_id=id, event=unicode('更新云平台信息')
                                           , submitter=g.username)
        return set_return_val(True, [], str('The platform information was updated successfully.'), 1520)

    @basic_auth.login_required
    def delete(self, id):
        """
        根据id删除云平台信息
       ---
       tags:
          - cloudplatform
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
            description: 删除平台信息
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
            control.cloud_platform.platform_delete(id)

        except Exception, e:
            return set_return_val(False, [], str(e), 1519), 400
        control.event_logs.eventlog_create(type='cloud_platform', result=True, resources_id=id, event=unicode('删除云平台信息')
                                           , submitter=g.username)
        return set_return_val(True, [], str('The platform information was deleted successfully.'), 1510)
