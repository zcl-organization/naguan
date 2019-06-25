# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter.control import network_port_group as network_manage
from app.main.base.apis.auth import basic_auth
from app.main.vcenter.control.network_port_group import PortGroup, DVSPortGroup

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('host_name')   # 创建端口组的host地址
parser.add_argument('switch_name')  # 创建或是删除的Switch名字 （包括DSwitch和VSwitch）
parser.add_argument('portgroup_id')  # 端口组id
parser.add_argument('portgroup_name')  # 端口组名称
parser.add_argument('port_num')  # 虚拟端口数量


class NetworkPortGroupManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
         获取vCenter network port group 信息 （vswitch）
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
                      host:
                        type: string
                        default: 192.168.12.203
                        description: host_system名称
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
            # print(e)
            return set_return_val(False, {}, 'Failed to get network group', 5701), 400
        return set_return_val(True, data, 'Get network group success', 5700)

    @basic_auth.login_required
    def post(self):
        """
         创建vCenter network port group 信息（vswitch）
        ---
       tags:
          - vCenter network port group
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
              - portgroup_name
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                host_name:
                  type: string
                  default: 192.168.12.203
                  description: 创建端口组的host地址
                  example: 192.168.12.203
                switch_name:
                  type: string
                  default: vSwitch0
                  description: 创建端口组关联的Switch名字
                  example: vSwitch0
                portgroup_name:
                  type: string
                  default: test_vswitch_portgroup
                  description: 端口组名称
                  example: test_vswitch_portgroup
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
                  default: "vm not found"
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            g.error_code = 5751
            args = parser.parse_args()

            if network_manage.check_if_portgroup_exists(
                portgroup_name=args['portgroup_name'], host_name=args['host_name']):
                g.error_code = 5752
                raise Exception("vSwitch network port group already exists")
            
            pg = PortGroup(args['platform_id'])
            pg.create_vswitch_portgroup(args['host_name'], args['switch_name'], args['portgroup_name'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Create network group', g.error_code), 400

        return set_return_val(True, [], "Create Network Group Success", 5750)

    @basic_auth.login_required
    def delete(self):
        """
         删除vCenter network port group 信息（vswitch）
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
            description: '1 -- platform_id'
          - in: query
            name: portgroup_id
            type: integer
            required: true
            description: '8 -- portgroup_id'
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
            g.error_code = 5801
            args = parser.parse_args()

            if not network_manage.check_if_portgroup_exists(portgroup_id=args['portgroup_id']):
                g.error_code = 5802
                raise Exception("vSwitch network port group does not exist")

            pg = PortGroup(args['platform_id'])
            pg.delete_vswitch_portgroup_by_id(args['portgroup_id'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Delete network group', g.error_code), 400

        return set_return_val(True, [], 'Delete Network Group Success', 5800)

    @basic_auth.login_required
    def put(self):
        pass


class NetworkDVSPortGroupManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
         获取vCenter network port group 信息 （dvswitch）
        ---
       tags:
          - vCenter network port group
       security:
       - basicAuth:
          type: http
          scheme: basic0
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
                      switch:
                        type: string
                        default: Dvswitch-test
                        description: 交换设备名称
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
            data = network_manage.get_dvs_network_port_group_all(args['platform_id'])
        except Exception as e:
            return set_return_val(False, {}, 'Failed to get network group', 5901), 400

        return set_return_val(True, data, 'Get network group success', 5900)

    @basic_auth.login_required
    def post(self):
        """
         创建vCenter network port group 信息（dvswitch）
        ---
       tags:
          - vCenter network port group
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
              - switch_name
              - portgroup_name
              - port_num
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                switch_name:
                  type: string
                  default: DSwitch-test
                  description: 创建端口组关联的Switch名字
                  example: DSwitch-test
                portgroup_name:
                  type: string
                  default: test_vswitch_portgroup
                  description: 端口组名称
                  example: test_vswitch_portgroup
                port_num:
                  type: integer
                  default: 4
                  description: 创建端口数量
                  example: 4
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
                  default: "vm not found"
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            g.error_code = 5951
            args = parser.parse_args()

            if network_manage.check_if_dvs_portgroup_exists(
                portgroup_name=args['portgroup_name'], switch_name=args['switch_name']):
                g.error_code = 5953
                raise Exception("dSwitch network port group already exists")

            pg = DVSPortGroup(args['platform_id'])
            pg.create_dvswitch_portgroup(args['switch_name'], args['portgroup_name'], int(args['port_num']))
        except Exception as e:
            return set_return_val(False, [], 'Failed to Create Dvswitch network group', g.error_code), 400
        
        return set_return_val(True, [], 'Create Dvswitch Network Group Success', 5950)

    @basic_auth.login_required
    def delete(self):
        """
         删除vCenter network port group 信息（dvswitch）
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
            description: '1 -- platform_id'
          - in: query
            name: portgroup_id
            type: integer
            required: true
            description: '8 -- portgroup_id'
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
            g.error_code = 6001
            args = parser.parse_args()

            if not network_manage.check_if_dvs_portgroup_exists(portgroup_id=args['portgroup_id']):
                g.error_code = 6003
                raise Exception("dSwitch network port group already exists")

            pg = DVSPortGroup(args['platform_id'])
            pg.delete_dvswitch_portgroup_by_id(args['portgroup_id'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Delete Dvswitch network group', g.error_code), 400

        return set_return_val(True, [], 'Delete Dvswitch Network Group Success', 6000)

    @basic_auth.login_required
    def put(self):
        pass
