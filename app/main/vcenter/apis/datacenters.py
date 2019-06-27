# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.base import control as base_control
from app.main.vcenter.control.datacenters import DataCenter

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('dc_name')
parser.add_argument('dc_id')


class DataCenterManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取vCenter DataCenter 信息
        ---
       tags:
          - vCenter DataCenter
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: integer
            required: false
          - in: query
            name: dc_name
            type: string
            required: false
          - in: query
            name: dc_id
            type: integer
            required: false
       responses:
          200:
            description: vCenter DataCenter 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: status
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      name:
                        type: string
                        default: DataCenter
                        description: DataCenter
                      mor_name:
                        type: string
                        default: datacenter-365
                        description: mor_name
                      platform_id:
                        type: integer
                        default: 1
                        description: platform_id
                      vm_nums:
                        type: integer
                        default: 1
                        description: vm_nums
                      cluster_nums:
                        type: integer
                        default: 1
                        description: cluster_nums
                      network_nums:
                        type: integer
                        default: 1
                        description: network_nums
                      datastore_nums:
                        type: integer
                        default: 1
                        description: datastore_nums
                      cpu_capacity:
                        type: integer
                        default: 0
                        description: cpu_capacity
                      used_cpu:
                        type: integer
                        default: 0
                        description: used_cpu
                      memory:
                        type: integer
                        default: 0
                        description: memory
                      used_memory:
                        type: integer
                        default: 0
                        description: used_memory
                      capacity:
                        type: integer
                        default: 1
                        description: capacity
                      used_capacity:
                        type: integer
                        default: 1
                        description: used_capacity
          400:
            description: 获取失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 1302
                msg:
                  type: string
                  default: "DataCenter not found"
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            datacenter = DataCenter(args['platform_id'])
            data = datacenter.list(args)
            # data = control.datacenters.find_datacenters(platform_id=args['platform_id'],
            #                                             dc_id=args['dc_id'], dc_name=args['dc_name'])
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001), 400
        return set_return_val(True, data, 'Datastore info get success.', 3000)

    @basic_auth.login_required
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
                  description: 数据中心名称
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
        args = parser.parse_args()
        data = dict(
            type='DataCenter',
            result=True,
            resources_id=None,
            event=unicode('创建datacenter'),
            submitter=g.username,
        )
        try:
            g.error_code = 4301
            if not all([args['platform_id'], args['dc_name']]):
                g.error_code = 4302
                raise Exception('Parameter error')
            if len(args['dc_name']) > 80:
                g.error_code = 4303
                raise ValueError("The name of the datacenter must be under 80 characters.")
            datacenter = DataCenter(args['platform_id'])
            dc_info = datacenter.create(args)
            # dc_id = control.datacenters.create_datacenter(
            #     platform_id=args.get('platform_id'), dc_name=args.get('dc_name'))
            data['resources_id'] = dc_info.id
        except Exception as e:
            data['result'] = False
            return set_return_val(False, data, str(e), g.error_code)
        finally:
            base_control.event_logs.eventlog_create(**data)

        return set_return_val(True, data, 'Datastore create success.', 4300)

    def put(self):
        pass

    @basic_auth.login_required
    def delete(self, id):
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
          - in: path
            type: integer
            format: int64
            name: id
            required: true
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
        data = dict(
            type='DataCenter',
            result=True,
            resources_id=id,
            event=unicode('删除datacenter'),
            submitter=g.username,
        )
        try:
            g.error_code = 4351
            args = parser.parse_args()
            if not all([args['platform_id'], id]):
                g.error_code = 4352
                raise Exception('Parameter error')

            datacenter = DataCenter(args['platform_id'])
            datacenter.delete(id)
        except Exception as e:
            data['result'] = False
            return set_return_val(False, data, str(e), g.error_code)
        finally:
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, data, 'Datastore delete success.', 4350)
