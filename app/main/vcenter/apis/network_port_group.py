# -*- coding:utf-8 -*-

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
            # print(e)
            return set_return_val(False, {}, 'Failed to get network group', 2461), 400
        return set_return_val(True, data, 'Get network group success', 2460)

    @basic_auth.login_required
    def post(self):
        """
        """
        try:
            args = parser.parse_args()

            if network_manage.check_if_portgroup_exists(args['portgroup_name'], args['host_name']):
                raise Exception
            
            pg = PortGroup(args['platform_id'])
            pg.create_vswitch_portgroup(args['host_name'], args['switch_name'], args['portgroup_name'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Create network group', 2463), 400

        return set_return_val(True, [], "Create Network Group Success", 2462)

    @basic_auth.login_required
    def delete(self):
        """
        """
        try:
            args = parser.parse_args()

            if not network_manage.check_if_portgroup_exists(args['portgroup_name'], args['host_name']):
                raise Exception

            pg = PortGroup(args['platform_id'])
            pg.delete_vswitch_portgroup_by_id(args['portgroup_id'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Delete network group', 2465), 400

        return set_return_val(True, [], 'Delete Network Group Success', 2464)

    @basic_auth.login_required
    def put(self):
        pass


class NetworkDVSPortGroupManage(Resource):
    @basic_auth.login_required
    def get(self):
        try:
            args = parser.parse_args()
            data = network_manage.get_dvs_network_port_group_all(args['platform_id'])
        except Exception as e:
            return set_return_val(False, {}, 'Failed to get network group', 2501), 400

        return set_return_val(True, data, 'Get network group success', 2500)

    @basic_auth.login_required
    def post(self):
        try:
            args = parser.parse_args()

            if network_manage.check_if_dvs_portgroup_exists(args['portgroup_name'], args['switch_name']):
                raise Exception

            pg = DVSPortGroup(args['platform_id'])
            pg.create_dvswitch_portgroup(args['switch_name'], args['portgroup_name'], args['port_num'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Create Dvswitch network group', 2501), 400
        
        return set_return_val(True, [], 'Create Dvswitch Network Group Success', 2500)

    @basic_auth.login_required
    def delete(self):
        try:
            args = parser.parse_args()

            if not network_manage.check_if_dvs_portgroup_exists(args['portgroup_name'], args['switch_name']):
                raise Exception

            pg = DVSPortGroup(args['platform_id'])
            pg.delete_dvswitch_portgroup(args['switch_name'], args['portgroup_name'])
        except Exception as e:
            return set_return_val(False, [], 'Failed to Delete Dvswitch network group', 2503), 400

        return set_return_val(True, [], 'Delete Dvswitch Network Group Success', 2502)

    @basic_auth.login_required
    def put(self):
        pass
