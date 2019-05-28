# -*- coding:utf-8 -*-
import json

from flask import g
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.vcenter.control.instances import Instance
from app.main.base import control as base_control

parser = reqparse.RequestParser()

parser.add_argument('platform_id')  # 云主机ID
parser.add_argument('vm_uuid')  # 虚拟机uuid
parser.add_argument('networks')  # 虚拟机uuid



class NetWorkManage(Resource):

    def get(self):
        """
         获取vCenter vm_network_device 信息
        ---
        tags:
          - vCenter network device
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
            if not all([args['platform_id'], args['vm_uuid']]):
                raise Exception('Parameter error')
            data = control.network_devices.get_network_by_vm_uuid(platform_id=args['platform_id'],
                                                                  vm_uuid=args['vm_uuid'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'network device gets success.', 1520)

    def post(self):
        """
         更新 vm  disk信息
        ---
        tags:
          - vCenter network device
        parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: query
            name: uuid
            type: string
            description: uuid
            required: true
          - in: query
            name: networks
            type: string
            description: '[1,2]--network_port_group_id'
            required: true
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
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            if args['networks']:
                instance.add_network(networks=args['networks'])
            for network in json.loads(args['networks']):
                datas.append(dict(type='vm_network', result=True, resources_id=args.get('vm_uuid'),
                                  event=unicode('添加网络，类型：%s' % network), submitter=g.username))
        except Exception as e:
            datas.append(dict(
                type='vm_network', result=False, resources_id=args.get('vm_uuid'),
                event=unicode('添加网络,类型：%s' % args.get('networks')), submitter=g.username
            ))
            return set_return_val(False, [], str(e), 1529), 400
        finally:
            [base_control.event_logs.eventlog_create(**item) for item in datas]
        return set_return_val(True, [], 'network update success.', 1520)

    def delete(self):
        """
         更新 vm  disk信息
        ---
        tags:
          - vCenter network device
        parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: query
            name: uuid
            type: string
            description: uuid
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
            resources_id='',
            event=unicode('删除网络,id：%s' % args.get('networks')),
            submitter=g.username,
        )
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            if args['networks']:
                instance.del_network(networks=args['networks'])
            data['result'] = True
        except Exception as e:
            # print(e)
            return set_return_val(False, [], str(e), 1529), 400
        finally:
            data['resources_id'] = args.get('vm_uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'network delete success.', 1520)
