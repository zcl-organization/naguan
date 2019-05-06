# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()

parser.add_argument('platform_id')  # 云主机ID
parser.add_argument('vm_uuid')  # 虚拟机uuid


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
            name: uuid
            type: string
            required: false
          - in: query
            name: vm_name
            type: string
            required: false
        responses:
          200:
            description: vCenter disk 信息
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
                      label:
                        type: string
                      disk_size:
                        type: string
                      disk_file:
                        type: string
                      level:
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
            data = control.network_devices.get_network_by_vm_uuid(platform_id=args['platform_id'], vm_uuid=args['vm_uuid'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'Datastore gets success.', 1520)