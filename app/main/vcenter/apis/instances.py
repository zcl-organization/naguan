# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base import control as base_control
from app.main.vcenter.control.instances import Instance

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
parser.add_argument('networks')
# parser.add_argument('del_networks')
parser.add_argument('dc_id')
parser.add_argument('ds_id')
parser.add_argument('disks')
# parser.add_argument('del_disks')
parser.add_argument('image_id')
parser.add_argument('snapshot_name')
parser.add_argument('description')
parser.add_argument('snapshot_id')
parser.add_argument('resourcepool')
parser.add_argument('ip')
parser.add_argument('subnet')
parser.add_argument('gateway')
parser.add_argument('dns')
parser.add_argument('domain')
parser.add_argument('guest_id')
parser.add_argument('pgnum')
parser.add_argument('pgsort')


class InstanceManage(Resource):
    def post(self):
        """
         操作 vm 信息
        ---
        tags:
          - vCenter instances
        parameters:
          - in: query
            name: platform_id
            type: string
            description: 云平台id
            required: true
          - in: query
            name: uuid
            type: string
            description: 云主机id
          - in: query
            name: action
            type: string
            description: 'start stop suspend remove restart create clone cold_migrate'
            required: true
          - in: query
            name: vm_name
            type: string
            description: 云主机名称
          - in: query
            name: new_cpu
            type: string
            description: new_cpu
          - in: query
            name: new_memory
            type: string
            description: new_memory
          - in: query
            name: host
            type: string
            description: host
          - in: query
            name: dc_id
            type: string
            description: datacenter id
          - in: query
            name: ds_id
            type: string
            description: datastore id
          - in: query
            name: resourcepool
            type: string
            description: resourcepool
          - in: query
            name: guest_id
            type: string
            description: guest_id
          - in: query
            name: image_id
            type: string
            description: image id
          - in: query
            name: disks
            type: string
            description: '[{"type":"thin","size":1},{"type":"thin","size":1}]'
          - in: query
            name: networks
            type: string
            description: '[1,2]--network_port_group_id'
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
            type='instances_vm',
            result=True,
            resources_id='',
            event=unicode('虚拟机操作'),
            submitter=g.username,
        )
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['uuid'])
            if args['action'] == 'start':
                data['event'] = unicode('开启虚拟机')
                instance.start()

            elif args['action'] == 'stop':
                data['event'] = unicode('关闭虚拟机')
                instance.stop()

            elif args['action'] == 'suspend':
                data['event'] = unicode('挂起虚拟机')
                instance.suspend()

            elif args['action'] == 'restart':
                data['event'] = unicode('重置虚拟机')
                instance.restart()

            elif args['action'] == 'create':
                data['event'] = unicode('创建虚拟机')
                instance.boot(new_cpu=args['new_cpu'], new_memory=args['new_memory'], dc_id=args['dc_id'],
                              ds_id=args['ds_id'], vm_name=args['vm_name'], networks=args['networks'],
                              disks=args['disks'], image_id=args['image_id'])

            elif args['action'] == 'clone':
                data['event'] = unicode('克隆虚拟机')
                instance.clone(new_vm_name=args['vm_name'], ds_id=args['ds_id'], dc_id=args['dc_id'],
                               resourcepool=args['resourcepool'])

            elif args['action'] == 'cold_migrate':
                data['event'] = unicode('虚拟机转化模板')
                instance.cold_migrate(host_name=args['host'], ds_id=args['ds_id'], dc_id=args['dc_id'],
                                      resourcepool=args['resourcepool'])

            elif args['action'] == 'ip_assignment':
                data['event'] = unicode('虚拟机分配ip地址')
                instance.ip_assignment(ip=args['ip'], subnet=args['subnet'],
                                       gateway=args['gateway'], dns=args['dns'], domain=args.get('domain'))

            else:
                data['result'] = False
                raise Exception('Parameter error')
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 1529), 400
        finally:
            data['resources_id'] = args.get('uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'instance action success.', 1520)

    # 获取 instance 列表
    def get(self):
        """
         获取 instance 信息
        ---
        tags:
          - vCenter instances
        parameters:
          - in: query
            name: platform_id
            type: string
            description: 平台id
            required: true
          - in: query
            name: host
            type: string
            description: host 名称
          - in: query
            name: vm_name
            type: string
            description: vmOcName
          - in: query
            name: pgsort
            type: string
            description: pgsort
          - in: query
            name: pgnum
            type: int
            description: 页码
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
                      cpu:
                        type: string
                        default: 2
                        description: cpu
                      created_at:
                        type: string
                        default: 2019-05-17 14:39:00
                        description: created_at
                      guest_full_name:
                        type: string
                        default: 'Red Hat Enterprise Linux 6 (64-bit)'
                        description: guest_full_name
                      guest_id:
                        type: string
                        default: rhel6_64Guest
                        description: guest_id
                      host:
                        type: string
                        default: 192.168.12.203
                        description: host
                      id:
                        type: string
                        default: 2
                        description: id
                      instance_uuid:
                        type: string
                        default: 500114bd-a861-f0ae-0f8d-f6e70d7c2c5c
                        description: instance_uuid
                      ip:
                        type: string
                        default: NUll
                        description: ip
                      memory:
                        type: string
                        default: 2048
                        description: memory
                      num_ethernet_cards:
                        type: string
                        default: 2
                        description: num_ethernet_cards
                      num_virtual_disks:
                        type: string
                        default: 2
                        description: num_virtual_disks
                      platform_id:
                        type: string
                        default: 2
                        description: platform_id
                      status:
                        type: string
                        default: poweredOff
                        description: status
                      template:
                        type: string
                        default: false
                        description: template
                      uuid:
                        type: string
                        default: 42018b9a-5e13-796b-02fa-57d6f56f3ac8
                        description: uuid
                      vm_mor_name:
                        type: string
                        default: vm-1362
                        description: vm_mor_name
                      vm_name:
                        type: string
                        default: 测试菜单1
                        description: vm_name
                      vm_path_name:
                        type: string
                        default: 测试菜单1
                        description: '[datastore1] 测试菜单1/测试菜单1.vmx'

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
            # print(args['pgnum'])
            pgnum = args['pgnum']
            if not pgnum:
                pgnum = 1  # 默认第一页
            # print(args['pgsort'])
            data, pg = instance.list(host=args['host'], vm_name=args['vm_name'], pgnum=pgnum,
                                     pgsort=args['pgsort'])
            # data = instance_manage.vm_list_all(platform_id=args['platform_id'], host=args['host'],
            #                                    vm_name=args['vm_name'])

        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'instance gets success.', 1520, pg)

    def delete(self, platform_id, uuid):
        """
        删除 vm 信息
        ---
        tags:
          - vCenter instances
        parameters:
          - in: path
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: path
            name: uuid
            type: string
            description: uuid
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
        data = dict(
            type='instances_vm',
            result=False,
            resources_id='',
            event=unicode('删除虚拟机'),
            submitter=g.username,
        )
        try:
            instance = Instance(platform_id=platform_id, uuid=uuid)
            instance.delete()
            data['result'] = True
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        finally:
            data['resources_id'] = uuid
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'instance delete success.', 1520)

    def put(self):
        """
         更新 vm 信息
        ---
        tags:
          - vCenter instances
        parameters:
          - in: path
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: path
            name: uuid
            type: string
            description: uuid
            required: true
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
            type='instances_vm',
            result=False,
            resources_id='',
            event=unicode('更新虚拟机'),
            submitter=g.username,
        )
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['uuid'])
            if all([args['new_cpu'], args['old_cpu']]):
                instance.update_vcpu(new_cpu=args['new_cpu'], old_cpu=args['old_cpu'])
                data['result'] = True

            if all([args['new_memory'], args['old_memory']]):
                instance.update_vmemory(new_memory=args['new_memory'], old_memory=args['old_memory'])
                data['result'] = True
            if not data['result']:
                raise Exception('parameter error')

            # # 添加网络
            # if args['new_networks']:
            #     instance.add_network(networks=args['new_networks'])
            #
            # if args['del_networks']:
            #     instance.del_network(networks=args['del_networks'])

            # if args['new_disks']:
            #     instance.add_disk(disks=args['new_disks'])
            #     # pass
            # if args['del_disks']:
            #     instance.delete_disk(disks=args['del_disks'])

            # if args['snapshot_name']:
            #     print(args['snapshot_name'])
            #     instance.add_snapshot(snapshot_name=args['snapshot_name'], description=args['description'])
            # if args['snapshot_id']:
            #     print(args['snapshot_id'])
            #     instance.delete_snapshot(snapshot_id=args['snapshot_id'])

        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        finally:
            data['resources_id'] = args.get('uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'instance update success.', 1520)
