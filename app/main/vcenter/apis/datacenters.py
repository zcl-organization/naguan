# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('dc_name')
parser.add_argument('dc_id')


class DataCenterManage(Resource):

    def post(self):
        """
         创建DataCenter信息
        ---
       tags:
          - vCenter DataCenter
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
              - platform_id
              - vm_uuid
              - snapshot_name
              - action
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                dc_name:
                  type: string
                  default: 1
                  description: 数据中心名
                  example: DataCenter
       responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "创建成功"
                data:
                  type: array
                  items:
                    properties:
          400:
            description: 创建失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "创建失败"
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            data = control.datacenters.create_datacenter(
                platform_id=args.get('platform_id'), dc_name=args.get('dc_name'))
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001)
        return set_return_val(True, data, 'Datastore create success.', 3000)

    def put(self):
        pass

    def delete(self):
        """
         删除DataCenter信息
        ---
       tags:
          - vCenter DataCenter
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
              - platform_id
              - vm_uuid
              - snapshot_name
              - action
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                dc_id:
                  type: string
                  default: 1
                  description: 数据中心id
                  example: 1
       responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "删除成功"
                data:
                  type: array
                  items:
                    properties:
          400:
            description: 创建失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "删除失败"
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            dc_id = args.get('dc_id')
            control.datacenters.del_datacenter(platform_id=args.get('platform_id'), dc_id=dc_id)
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001)
        return set_return_val(True, {}, 'Datastore delete success.', 3000)


