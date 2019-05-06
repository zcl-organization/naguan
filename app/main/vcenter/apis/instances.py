# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter.control import instances as instance_manage
from app.main.vcenter.control.instances import Instance
import json

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('host')
parser.add_argument('vm_name')
parser.add_argument('action')
parser.add_argument('uuid')
parser.add_argument('new_cpu')
parser.add_argument('old_cpu')
parser.add_argument('new_memory')
parser.add_argument('old_memory')
parser.add_argument('new_networks')
parser.add_argument('del_networks')
parser.add_argument('dc_id')
parser.add_argument('ds_id')
parser.add_argument('new_disks')
parser.add_argument('del_disks')
parser.add_argument('image_id')

ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': {}
}


class InstanceManage(Resource):
    def post(self):
        """
         操作 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: query
            name: action
            type: string
            description: '操作云主机 start stop suspend remove restart create'
          - in: query
            name: vm_name
            type: string
            description: 云主机名称
          - in: query
            name: platform_id
            type: string
            description: 云平台id
          - in: query
            name: uuid
            type: string
            description: 云主机id
          - in: query
            name: cpu
            type: string
            description: new_cpu
          - in: query
            name: memory
            type: string
            description: new_memory
          - in: query
            name: ds_id
            type: string
            description: datastore id
          - in: query
            name: image_id
            type: string
            description: image id
          - in: query
            name: new_disk
            type: string
            description: [{"type":"thin","size":1},{"type":"thin","size":1}]
          - in: query
            name: net_network
            type: string
            description: [1,2] -- network_port_group_id
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
                      id:
                        type: string
                        default: 1
                      vmtitle:
                        type: string
                      vmMorName:
                        type: string
                      vmOcName:
                        type: string
                      toolsVersion:
                        type: string
                      toolsRun:
                        type: string
                      sys:
                        type: string
                      poolMorName:
                        type: string
                      poolOcName:
                        type: string
                      kvmVVType:
                        type: string
                      isThin:
                        type: string
                      ip:
                        type: string
                      hostMorName:
                        type: string
                      hostOcName:
                        type: string
                      hSpace:
                        type: string
                      dSpace:
                        type: string
                      cpuHzRate:
                        type: string
                      cpuHzOverhead:
                        type: string
                      cpu:
                        type: string
                      State:
                        type: string
                      Network:
                        type: string
                      MemoryRate:
                        type: string
                      Memory:
                        type: string
                      DiskRate:
                        type: string
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
        # print(args)
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['uuid'])

            if args['action'] == 'start':
                instance.start()

            elif args['action'] == 'stop':
                instance.stop()

            elif args['action'] == 'suspend':
                instance.suspend()

            elif args['action'] == 'restart':
                instance.restart()

            elif args['action'] == 'create':
                # print(args['new_disks'])
                # disks = json.loads(args['new_disks'])
                #
                # for disk in disks:
                #     disk_size = disk.get('size')
                #     disk_type = disk.get('type')
                #     print(disk_type)

                instance.boot(new_cpu=args['new_cpu'], new_memory=args['new_memory'], dc_id=args['dc_id'],
                              ds_id=args['ds_id'], vm_name=args['vm_name'], networks=args['new_networks'],
                              disks=args['new_disks'], image_id=args['image_id'])
            else:
                raise Exception('Parameter error')
        except Exception as e:
            print('raise ', e)
        return "操作成功"

    # 获取 instance 列表
    def get(self):
        """
         获取 instance 信息
        ---
        tags:
          - instances
        parameters:
          - in: query
            name: mor_name
            type: string
            description: host 名称
          - in: query
            name: platform_id
            type: string
            description: 平台id
          - in: query
            name: vm_name
            type: string
            description: vmOcName
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
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 1
                      vmtitle:
                        type: string
                      vmMorName:
                        type: string
                      vmOcName:
                        type: string
                      toolsVersion:
                        type: string
                      toolsRun:
                        type: string
                      sys:
                        type: string
                      poolMorName:
                        type: string
                      poolOcName:
                        type: string
                      kvmVVType:
                        type: string
                      isThin:
                        type: string
                      ip:
                        type: string
                      hostMorName:
                        type: string
                      hostOcName:
                        type: string
                      hSpace:
                        type: string
                      dSpace:
                        type: string
                      cpuHzRate:
                        type: string
                      cpuHzOverhead:
                        type: string
                      cpu:
                        type: string
                      State:
                        type: string
                      Network:
                        type: string
                      MemoryRate:
                        type: string
                      Memory:
                        type: string
                      DiskRate:
                        type: string
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
        try:
            instance = Instance(platform_id=args['platform_id'])
            data = instance.list(host=args['host'], vm_name=args['vm_name'])
            # data = instance_manage.vm_list_all(platform_id=args['platform_id'], host=args['host'],
            #                                    vm_name=args['vm_name'])

        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'instance gets success.', 1520)

    def delete(self, platform_id, uuid):
        """
         操作 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: path
            name: platform_id
            type: string
            description: platform_id
          - in: path
            name: uuid
            type: string
            description: uuid
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
            description: 删除失败
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
                  default: "删除失败"
                data:
                  type: array
                  items:
                    properties:
        """
        # args = parser.parse_args()
        try:
            instance = Instance(platform_id=platform_id, uuid=uuid)
            instance.delete()
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, [], 'instance delete success.', 1520)



    def put(self):
        """
         更新 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: path
            name: platform_id
            type: string
            description: platform_id
          - in: path
            name: uuid
            type: string
            description: uuid
          - in: query
            name: new_disks
            type: string
            description: '[{"type":"thin","size":1},{"type":"thin","size":1}]'
          - in: query
            name: del_disks
            type: string
            description: '[1,2]'
          - in: query
            name: new_networks
            type: string
            description: '[1,2]--network_port_group_id'
          - in: query
            name: del_networks
            type: string
            description: '[1,2]--network_device_id'
          - in: query
            name: new_cpu
            type: string
            description: new_cpu
          - in: query
            name: old_cpu
            type: string
            description: old_cpu
          - in: query
            name: new_memory
            type: string
            description: new_memory
          - in: query
            name: old_memory
            type: string
            description: old_memory
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
                      id:
                        type: string
                        default: 1
                      vmtitle:
                        type: string
                      vmMorName:
                        type: string
                      vmOcName:
                        type: string
                      toolsVersion:
                        type: string
                      toolsRun:
                        type: string
                      sys:
                        type: string
                      poolMorName:
                        type: string
                      poolOcName:
                        type: string
                      kvmVVType:
                        type: string
                      isThin:
                        type: string
                      ip:
                        type: string
                      hostMorName:
                        type: string
                      hostOcName:
                        type: string
                      hSpace:
                        type: string
                      dSpace:
                        type: string
                      cpuHzRate:
                        type: string
                      cpuHzOverhead:
                        type: string
                      cpu:
                        type: string
                      State:
                        type: string
                      Network:
                        type: string
                      MemoryRate:
                        type: string
                      Memory:
                        type: string
                      DiskRate:
                        type: string
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

        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['uuid'])
            if all([args['new_cpu'], args['old_cpu']]):
                instance.update_vcpu(new_cpu=args['new_cpu'], old_cpu=args['old_cpu'])

            if all([args['new_memory'], args['old_memory']]):
                instance.update_vmemory(new_memory=args['new_memory'], old_memory=args['old_memory'])

            # 添加网络
            if args['new_networks']:
                instance.add_network(networks=args['new_networks'])

            if args['del_networks']:
                instance.del_network(networks=args['del_networks'])

            if args['new_disks']:
                instance.add_disk(disks=args['new_disks'])
                # pass
            if args['del_disks']:
                instance.delete_disk(disks=args['del_disks'])
        except Exception as e:
            # print(e)
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, [], 'instance update success.', 1520)
