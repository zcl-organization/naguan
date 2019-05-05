# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

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
parser.add_argument('delete_disks')

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
            description: '操作云主机 start stop suspend remove restart'
          - in: query
            name: vmname
            type: string
            description: 云主机名称
          - in: query
            name: platform_id
            type: string
            description: 云平台id
          - in: query
            name: cpu
            type: string
            description: cpu
          - in: query
            name: memory
            type: string
            description: memory
          - in: query
            name: dc_mor_name
            type: string
            description: datacenter mor name
          - in: query
            name: image_type
            type: string
            description: 镜像类型
          - in: query
            name: arrDiskInputJson
            type: string
            description: '[{"diskInput":"1"}]'
          - in: query
            name: arrIsThinJson
            type: string
            description: '[{"isThin":"true"}]'
          - in: query
            name: arrDiskOcNameJson
            type: string
            description: '[{"diskOcName":"Local_62"}]'
          - in: query
            name: arrNetNameJson
            type: string
            description: '[{"netName":"VM Network"}]'
          - in: query
            name: hostOcName
            type: string
            description: host name
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
                              disks=args['new_disks'])
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
            ret_status['ok'] = True
            ret_status['code'] = 1111
            ret_status['data'] = data
            ret_status['msg'] = '查询成功'
        except Exception as e:
            ret_status['ok'] = False
            ret_status['code'] = 1111
            ret_status['data'] = {}
            ret_status['msg'] = '查询失败'
            return ret_status, 400
        return ret_status

    def delete(self, platfrom_id, uuid):
        """
         操作 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: path
            name: id
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
        args = parser.parse_args()
        instance = Instance(platform_id=platfrom_id, uuid=uuid)
        instance.delete()

        return '删除成功'

    def put(self):
        """
         更新 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: path
            name: id
            type: string
            description: platform_id
          - in: path
            name: uuid
            type: string
            description: uuid
          - in: query
            name: arrDiskOcNameJson
            type: string
            description: '[{"diskOcName":"Local_62"}]'
          - in: query
            name: arrNetNameJson
            type: string
            description: '[{"netName":"VM Network"}]'
          - in: query
            name: cpu
            type: string
            description: cpu
          - in: query
            name: memory
            type: string
            description: memory
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
            if args['delete_disks']:
                instance.delete_disk(disks=args['delete_disks'])
        except Exception as e:
            print(e)
            return 'vm update failed', 400
        return 'vm update success'
