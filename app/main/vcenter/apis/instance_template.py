# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app import set_return_val
from app.main.vcenter import control
from app.main.base import control as base_control


parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('pgnum')  # 翻页
parser.add_argument('pgsort')
parser.add_argument('host')
parser.add_argument('vm_name')

parser.add_argument('template_uuid')
parser.add_argument('dc_id')  # 数据中心
parser.add_argument('ds_id')  # 数据存储
parser.add_argument('resource_pool_id')  # 资源中心
parser.add_argument('host_id')  # host


class InstanceTemplateManage(Resource):

    def get(self):
        """
         获取 instance模板 信息
        ---
       tags:
          - vCenter instance_template
       security:
       - basicAuth:
          type: http
          scheme: basic
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
            description: vCenter instance_template 信息
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
                        default: true
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
            if not args['platform_id']:
                raise Exception('Parameter error')
            instance = control.instances.Instance(platform_id=args['platform_id'])

            pgnum = args['pgnum'] if args['pgnum'] else 1

            data, pg = instance.list(host=args['host'], vm_name=args['vm_name'], pgnum=pgnum,
                                     pgsort=args['pgsort'], template=True)
        except Exception as e:
            return set_return_val(False, [], str(e), 2031), 400
        return set_return_val(True, data, 'instance gets success.', 2030, pg), 200

    def post(self):
        """
         模板创建vm信息
        ---
       tags:
          - vCenter instance_template
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
              - template_uuid
              - vm_name
              - ds_id
              - dc_id
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                template_uuid:
                  type: string
                  default: 42016538-e4d6-e46f-782f-5a9f091ab221
                  description: 模板uuid
                  example: 42016538-e4d6-e46f-782f-5a9f091ab221
                vm_name:
                  type: string
                  default: xinjianvm
                  description: 新vm名称
                  example: xinjianvm
                ds_id:
                  type: integer
                  default: 1
                  description: DataStore id
                  example: 1
                dc_id:
                  type: integer
                  default: 1
                  description: datacenter id
                  example: 1
          - in: path
            name: resource_pool_id
            type: integer
            format: int64
          - in: path
            name: host_id
            type: integer
            format: int64
       responses:
          200:
            description: vCenter instance_template 信息
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
            type='instance_template',
            result=True,
            resources_id='',
            event=unicode('模板创建虚拟机'),
            submitter=g.username,
        )
        try:
            if not all([args['platform_id'], args['template_uuid'], args['vm_name'],
                        args['ds_id'], args['dc_id']]):
                raise Exception('Parameter error')
            instance_vm_template = control.instance_template.InstanceVmTemplate(
                platform_id=args['platform_id'], uuid=args['template_uuid'])
            instance_vm_template.template_create_vm(new_vm_name=args['vm_name'], ds_id=args['ds_id'],
                                                    dc_id=args['dc_id'], resource_pool_id=args.get('resource_pool_id'),
                                                    host_id=args.get('host_id'))
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 2031), 400
        finally:
            data['resources_id'] = args.get('template_uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'Template to virtual machine success.', 2030), 200

    def delete(self, vm_uuid):
        pass
