# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter.control.vswitch import get_vswitch_infos, check_if_vswitch_exists
from app.main.vcenter.control.vswitch import VSwitch


parser = reqparse.RequestParser()
parser.add_argument('platform_id')  # 平台ID
parser.add_argument('host_name')   # hostsystem 名称      TODO 修改为host——id 待表构建完成
parser.add_argument('switch_name')  # 创建或是修改或是删除的交换机名称
parser.add_argument('num_port')   # 设置端口组大小
parser.add_argument('mtu')    # 设置mtu时钟时间
parser.add_argument('nics')   # 物理卡设备列表


class VSwitchManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取 vSwitch 信息
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
                raise RuntimeError('Parameter Error!!!')

            data = get_vswitch_infos(args['platform_id'])
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001), 400

        return set_return_val(True, data, 'Get Vswitch Info Success!!!', 3000)

    @basic_auth.login_required
    def post(self):
        """
          创建vSwitch
        ---
       tags:
          - vCenter vSwitch
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

            if not all([args['platform_id'], args['host_name'], args['switch_name']]):
                raise RuntimeError('Parameter Error!!!')

            vsw = VSwitch(args['platform_id'])
            vsw.create_vswitch(args)
        except Exception as e:
            return set_return_val(False, [], str(e), 3003), 400
        
        return set_return_val(True, [], 'Create Vswitch Success!!!', 3002)

    @basic_auth.login_required
    def delete(self, vswitch_id):
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

            vsw = VSwitch(args['platform_id'])
            vsw.delete_vswitch_by_id(vswitch_id)
        except Exception as e:
            return set_return_val(False, [], str(e), 3005), 400

        return set_return_val(True, [], 'Delete Vswitch Success!!!', 3004)

    @basic_auth.login_required
    def put(self, vswitch_id):
        """
          更新vSwitch
        ---
       tags:
          - vCenter vSwitch
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: path
            name: vswiter_id
            type: integer
            required: true
            description: '8 -- vswiter_id'
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
            description: vCenter vSwitch 修改状态信息
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
            description: 修改失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 3007
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            if not all([args['host_name'], args['switch_name']]):
                raise RuntimeError('Parameter Error!!!')

            vsw = VSwitch(args['platform_id'])
            vsw.update_vswich(vswitch_id, args)
        except Exception as e:
            return set_return_val(False, [], str(e), 3007)

        return set_return_val(True, {}, 'Update Vswitch Success!!!', 3006)
