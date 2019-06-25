# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import g

from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter.control.dvswitch import get_dvswitch_infos
from app.main.vcenter.control.dvswitch import DVSwitch


parser = reqparse.RequestParser()
parser.add_argument('platform_id')  # 平台ID
parser.add_argument('dc_name')  # datacenter名称
parser.add_argument('switch_name')  # 创建或是修改或是删除的交换机名称

parser.add_argument('mtu')    # 设置mtu时钟时间
parser.add_argument('protocol')    # 发现协议类型
parser.add_argument('operation')    # 发现协议操作
parser.add_argument('uplink_quantity')    # 上传链路组数量
parser.add_argument('uplink_prefix')    # 上传链路组前缀名称
parser.add_argument('switch_version')    # 交换机版本设置

parser.add_argument("old_uplink_name")  # 修改前的单个上传链路名称
parser.add_argument("new_uplink_name")  # 修改后的单个上传链路名称



class DVSwitchManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
           查询DVSwitch
        ---
       tags:
          - vCenter DVSwitch
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
                      host_id:
                        type: list
                        default: [1, 2, 3]
                        description: 主机编号
                      protocol:
                        type: string
                        default: cdp
                        description: 发现协议类型
                      operation:
                        type: string
                        default: "listen"
                        description: 发现协议操作
                      admin_name:
                        type: string
                        default: "admin"
                        description: 管理员名称
                      admin_describe:
                        type: string
                        default: "balabala..."
                        description: 管理员相关描述
                      describe:
                        type: string
                        default: "balabala..."
                        description: 描述
                      version:
                        type: string
                        default: "6.6.0"
                        description: 版本
                      mulit_mode:
                        type: string
                        default: "legacyFiltering"
                        description: 多拨筛选模式
                      active_uplink_port:
                        type: list
                        default: ["uplink 1", "uplink2"]
                        description: 活动上行链路组
                      standby_uplink_port:
                        type: list
                        default: []
                        description: 未启用的上行链路组
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
                  default: 6501
                msg:
                  type: string
                  default: ""
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            g.error_code = 6501
            args = parser.parse_args()
            if not args['platform_id']:
                g.error_code = 6502
                raise RuntimeError('Parameter Error!!!')

            data = get_dvswitch_infos(args['platform_id'])
        except Exception as e:
            return set_return_val(False, {}, str(e), g.error_code), 400

        return set_return_val(True, data, 'Get Dvswitch Info Success!!!', 6500)

    @basic_auth.login_required
    def post(self):
        """
          创建DVSwitch
        ---
       tags:
          - vCenter DVSwitch
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
              - dc_name
              - switch_name
              - mtu
              - protocol
              - operation
              - uplink_quantity
              - uplink_prefix
              - switch_version
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                dc_name:
                  type: string
                  default: Datacenter
                  description: DC名称
                  example: Datacenter
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
                protocol:
                  type: string
                  default: "cdp"
                  description: 发现协议类型
                  example: "cdp"
                operation:
                  type: string
                  default: "listen"
                  description: 发现协议操作
                  example: "listen"
                uplink_quantity:
                  type: integer
                  default: 4
                  description: 上传链路数量设置
                  example: 4
                uplink_prefix:
                  type: string
                  default: "dvs"
                  description: 上传链路前缀名称
                  example: "dvs"
                switch_version:
                  type: string
                  default: "6.6.0"
                  description: 交换机版本设置
                  example: "6.6.0"
       responses:
          200:
            description: vCenter DVSwitch 创建状态信息
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
            g.error_code = 6551
            args = parser.parse_args()

            if not all([args['platform_id'], args['switch_name'], args['dc_name']]):
                g.error_code = 6552
                raise RuntimeError('Parameter Error!!!')

            dvsw = DVSwitch(args['platform_id'])
            dvsw.create_dvswitch(args)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        
        return set_return_val(True, [], 'Create Vswitch Success!!!', 6550)

    @basic_auth.login_required
    def delete(self, dvswitch_id):
        """
         删除DVSwitch
        ---
       tags:
          - vCenter DVSwitch
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
            name: dvswitch_id
            type: integer
            required: true
            description: '8 -- switer_id'
       responses:
          200:
            description: vCenter DVSwitch 信息
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
            g.error_code = 6601
            args = parser.parse_args()

            if not args['platform_id']:
                g.error_code = 6602
                raise RuntimeError('Parameter Error!!!')

            dvsw = DVSwitch(args['platform_id'])
            # dvsw.delete_dvswitch_by_name("test", 'Datacenter')
            dvsw.delete_dvswitch_by_id(dvswitch_id)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400

        return set_return_val(True, [], 'Delete Vswitch Success!!!', 6600)

    @basic_auth.login_required
    def put(self, dvswitch_id):
        """
        更新DVSwitch
        ---
       tags:
          - vCenter DVSwitch
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: path
            name: dvswitch_id
            type: integer
            required: true
            description: '8 -- dvswitch_id'
          - in: body
            name: body
            required: true
            schema:
              required:
              - platform_id
              - mtu
              - protocol
              - operation
              - old_uplink_name
              - new_uplink_name
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                mtu:
                  type: integer
                  default: 1500
                  description: 交换机mtu设置
                  example: 1500
                protocol:
                  type: string
                  default: "cdp"
                  description: 发现协议类型
                  example: "cdp"
                operation:
                  type: string
                  default: "listen"
                  description: 发现协议操作
                  example: "listen"
                old_uplink_name:
                  type: string
                  default: "dvs 1"
                  description: 修改前的上行链路名称
                  example: "dvs 1"
                new_uplink_name:
                  type: string
                  default: "amd_yes"
                  description: 修改后的上行链路名称
                  example: "amd_yes"
       responses:
          200:
            description: vCenter DVSwitch 修改状态信息
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
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            g.error_code = 6651
            args = parser.parse_args()
            if not all([args['platform_id'],]):
                g.error_code = 6652
                raise RuntimeError('Parameter Error!!!')

            dvsw = DVSwitch(args['platform_id'])
            dvsw.update_dvswich(dvswitch_id, args)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code)

        return set_return_val(True, {}, 'Update Vswitch Success!!!', 6650)
