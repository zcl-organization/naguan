# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter.control.host import Host

parser = reqparse.RequestParser()
parser.add_argument('platform_id')  # 平台ID
parser.add_argument('new_host_name')  # hostsystem 名称


class ResourceHostManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取 Host 信息
        ---
       tags:
          - vCenter Host
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
            description: vCenter vSwitch 信息
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
                      nics:
                        type: list
                        default: ['vemic0',]
                        description: nics
                      num_of_port:
                        type: string
                        default: 128
                        description: numPorts
                      mtu:
                        type: integer
                        default: 1500
                        description: mtu
                      host_name:
                        type: string
                        default: 192.168.12.203
                        description: host_name
                      host_mor_name:
                        type: string
                        default: 'hostsystem-890'
                        description: host_mor_name
                      name:
                        type: string
                        default: mu_test
                        description: name
                      platform_id:
                        type: interger
                        default: 1
                        description: platform_id
                      id:
                        type: string
                        default: 1
                        description: id
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
                  default: 3001
                msg:
                  type: string
                  default: ""
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            if not args['platform_id']:
                raise RuntimeError('Parameter Error!')
            # TODO 功能未做
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001), 400

        return set_return_val(True, [], 'Get Info Success!', 3000)

    # @basic_auth.login_required
    def post(self):
        """
          创建Host
        ---
       tags:
          - vCenter Host
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
              - host_name
              - switch_name
              - mtu
              - num_port
              - nics
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                host_name:
                  type: string
                  default: 192.168.12.203
                  description: 主机名称
                  example: 192.168.12.203
                switch_name:
                  type: string
                  default: test_vs
                  description: vswitch交换机名称
                  example: test_vs
                mtu:
                  type: integer
                  default: 1500
                  description: 交换机mtu设置
                  example: 1500
                num_port:
                  type: integer
                  default: 128
                  description: 交换机端口数量
                  example: 128
                nics:
                  type: list
                  default: ["vmnic3",]
                  description: 上行链路组
                  example: ["vmnic3",]
       responses:
          200:
            description: vCenter vSwitch 创建状态信息
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
                  default: 3002
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()

            if not all([args['platform_id'], args['new_host_name']]):
                raise RuntimeError('Parameter Error!!!')

            host = Host(args['platform_id'])
            host.add_host(args['new_host_name'])
        except Exception as e:
            return set_return_val(False, [], str(e), 3001), 400

        return set_return_val(True, [], 'Create Host Success!!!', 3000)

    @basic_auth.login_required
    def delete(self):
        """
         删除vSwitch
        ---
       tags:
          - vCenter vSwitch
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
            description: '1 -- platform_id'
          - in: path
            name: vswiter_id
            type: integer
            required: true
            description: '8 -- vswiter_id'
       responses:
          200:
            description: vCenter vSwitch 信息
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
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            if not args['platform_id']:
                raise RuntimeError('Parameter Error!!!')
        except Exception as e:
            return set_return_val(False, [], str(e), 3001), 400

        return set_return_val(True, [], 'Delete Success!!!', 3000)

    @basic_auth.login_required
    def put(self):
        pass
