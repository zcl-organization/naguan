# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.vcenter.control.instances import Instance

parser = reqparse.RequestParser()

parser.add_argument('platform_id')  # 云主机ID
parser.add_argument('vm_uuid')  # 虚拟机uuid


class DiskManage(Resource):

    def get(self):
        """
         获取vCenter vm_disk 信息
        ---
        tags:
          - vCenter disk
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
            description: vCenter disk 信息
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
                      cache:
                        type: string
                        default: 200
                        description: cache
                      disk_file:
                        type: string
                        default: '[ssd-1]clone2/clone2.vmdk'
                        description: disk_file
                      disk_mode:
                        type: string
                        default: persistent
                        description: disk_mode
                      disk_size:
                        type: string
                        default: 54,525,952 KB
                        description: disk_size
                      disk_type:
                        type: integer
                        default: Provisioned
                        description: disk_type
                      disk_uuid:
                        type: string
                        default: 6000C298-91e2-7c1d-d4b6-0b53feba44bd
                        description: disk_uuid
                      id:
                        type: string
                        default: 43
                        description: id
                      iops:
                        type: string
                        default: -1
                        description: iops
                      label:
                        type: string
                        default: Hard disk 1
                        description: label
                      level:
                        type: string
                        default: normal
                        description: level
                      platform_id:
                        type: string
                        default: 1
                        description: platform_id
                      shares:
                        type: string
                        default: 1000
                        description: shares
                      sharing:
                        type: string
                        default: sharingNone
                        description: sharing
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
        # platform_id = args.get('platform_id')
        # vm_uuid = args.get('vm_uuid')
        try:
            if not all([args['platform_id'], args['vm_uuid']]):
                raise Exception('Parameter error')
            data = control.disks.get_disk_by_vm_uuid(platform_id=args['platform_id'], vm_uuid=args['vm_uuid'])
        except Exception as e:
            return set_return_val(False, [], str(e), 2131), 400
        return set_return_val(True, data, 'Datastore gets success.', 2130)

    def post(self):
        """
         更新 vm  disk信息
        ---
        tags:
          - vCenter disk
        parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
          - in: query
            name: uuid
            type: string
            description: uuid
          - in: query
            name: disks
            type: string
            description: '[{"type":"thin","size":1},{"type":"thin","size":1}]'
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

        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            if not args['disks']:
                raise Exception('Parameter error')
            instance.add_disk(disks=args['disks'])

        except Exception as e:
            return set_return_val(False, [], str(e), 2101), 400
        return set_return_val(True, [], 'Instance attack disk successfully.', 2100)

    def delete(self):
        """
         更新 vm  disk信息
        ---
        tags:
          - vCenter disk
        parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
          - in: query
            name: vm_uuid
            type: string
            description: vm_uuid
          - in: query
            name: disks
            type: string
            description: '[1,2]'
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
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])

            if not args['disks']:
                raise Exception('Parameter error')
            instance.delete_disk(disks=args['disks'])
        except Exception as e:
            return set_return_val(False, [], str(e), 2111), 400
        return set_return_val(True, [], 'Instance deattach disk successfully', 2110)
