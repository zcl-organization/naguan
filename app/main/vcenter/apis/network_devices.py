# -*- coding:utf-8 -*-
import json

from flask import g
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.vcenter.control.instances import Instance

from app.main.base import control as base_control
from app.main.base.apis.auth import basic_auth

parser = reqparse.RequestParser()

parser.add_argument('platform_id')  # 云主机ID
parser.add_argument('vm_uuid')  # 虚拟机uuid
parser.add_argument('networks')


class NetWorkManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取vCenter vm_network_device 信息
        ---
       tags:
          - vCenter network device
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
          - in: query
            name: vm_uuid
            type: string
            required: true
       responses:
          200:
            description: vCenter network device  信息
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
                data:
                  type: array
                  items:
                    properties:
                      address_type:
                        type: string
                        default: assigned
                        description: address_type
                      id:
                        type: string
                        default: 1
                        description: id
                      label:
                        type: string
                        default: Network adapter 1
                        description: label
                      mac:
                        type: string
                        default: 00:50:56:81:bd:78
                        description: mac
                      network_port_group:
                        type: string
                        default: VM Network
                        description: network_port_group
                      platform_id:
                        type: string
                        default: 1
                        description: platform_id
                      vm_uuid:
                        type: string
                        default: 42018ddf-f886-12b5-a652-dd60b04ca2df
                        description: vm_uuid
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
                  default: "vm not found"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        try:
            g.error_code = 4901
            if not all([args['platform_id'], args['vm_uuid']]):
                g.error_code = 4902
                raise Exception('Parameter error')
            data = control.network_devices.get_network_by_vm_uuid(platform_id=args['platform_id'],
                                                                  vm_uuid=args['vm_uuid'])
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        return set_return_val(True, data, 'network device gets success.', 4900)

    @basic_auth.login_required
    def post(self):
        """
         更新 vm  disk信息
        ---
       tags:
          - vCenter network device
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
              - networks
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                vm_uuid:
                  type: integer
                  default: 2018ddf-f886-12b5-a652-dd60b04ca2df
                  description: 云主机uuid
                  example: 2018ddf-f886-12b5-a652-dd60b04ca2df
                networks:
                  type: dict
                  default: '{"dvswitch": [1,2], "vswitch": [1,2]}'
                  description: '{"dvswitch": [1,2], "vswitch": [1,2]}--network_port_group_id'
                  example: '{"dvswitch": [1,2], "vswitch": [1,2]}'

       responses:
          200:
            description:  vm 添加 network device  信息
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
                  default: "操作成功"
                data:
                  type: array
                  items:
                    properties:
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
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """

        args = parser.parse_args()
        datas = []
        try:
            g.error_code = 4951
            if not args['networks']:
                g.error_code = 4952
                raise Exception('Parameter error')
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            instance.add_network(networks=args['networks'])
            for network in json.loads(args['networks']):
                datas.append(dict(type='vm_network', result=True, resources_id=args.get('vm_uuid'),
                                  event=unicode('添加网络，类型：%s' % network), submitter=g.username))
        except Exception as e:

            datas.append(dict(
                type='vm_network', result=False, resources_id=args.get('vm_uuid'),
                event=unicode('添加网络,类型：%s' % args.get('networks')), submitter=g.username
            ))
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            [base_control.event_logs.eventlog_create(**item) for item in datas]
        return set_return_val(True, [], 'network update success.', 4950)

    @basic_auth.login_required
    def delete(self):
        """
         更新 vm  disk信息
        ---
       tags:
          - vCenter network device
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: query
            name: vm_uuid
            type: string
            description: vm_uuid
            required: true
          - in: query
            name: networks
            type: string
            description: '[1,2]--network_device_id'
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
                  default: "操作成功"
                data:
                  type: array
                  items:
                    properties:
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
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        data = dict(
            type='vm_network',
            result=False,
            resources_id=None,
            event=unicode('删除网络,id：%s' % args.get('networks')),
            submitter=g.username,
        )
        try:
            g.error_code = 5001
            if not args['networks']:
                g.error_code = 5002
                raise Exception('Parameter error')
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            instance.del_network(networks=args['networks'])
            data['result'] = True
        except Exception as e:
            # print(e)

            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = args.get('vm_uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'network delete success.', 5000)
