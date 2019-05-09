# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter.control import network_port_group as network_manage
parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class NetworkPortGroupManage(Resource):

    def get(self):
        """
         获取vCenter vm_network_device 信息
        ---
        tags:
          - vCenter network port group
        parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
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
        try:
            args = parser.parse_args()
            data = network_manage.get_network_port_group_all(args['platform_id'])
        except Exception as e:
            print(e)
            return set_return_val(False, {}, 'Failed to get network group', 1239), 400
        return set_return_val(True, data, 'Get network group success', 1230)

    def post(self):
        args = parser.parse_args()
        # platform_id
        # uuid
        # network_id
        # network_manage.

    def put(self):
        pass

    def delete(self):
        pass



