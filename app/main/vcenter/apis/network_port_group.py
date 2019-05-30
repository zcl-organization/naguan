# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter.control import network_port_group as network_manage
from app.main.base.apis.auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class NetworkPortGroupManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
         获取vCenter network port group 信息
        ---
       tags:
          - vCenter network port group
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
       responses:
          200:
            description: vCenter port group 信息
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
                      dc_mor_name:
                        type: string
                        default: datacenter-661
                        description: dc_mor_name
                      dc_name:
                        type: string
                        default: Datacenter
                        description: dc_name
                      id:
                        type: string
                        default: 1
                        description: id
                      mor_name:
                        type: string
                        default: dvportgroup-1284
                        description: mor_name
                      name:
                        type: string
                        default: NSX-DVUplinks-1283
                        description: name
                      platform_id:
                        type: string
                        default: 1
                        description: platform_id
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
            return set_return_val(False, {}, 'Failed to get network group', 2461), 400
        return set_return_val(True, data, 'Get network group success', 2460)

    @basic_auth.login_required
    def post(self):
        args = parser.parse_args()
        # platform_id
        # uuid
        # network_id
        # network_manage.

    @basic_auth.login_required
    def put(self):
        pass
    @basic_auth.login_required
    def delete(self):
        pass



