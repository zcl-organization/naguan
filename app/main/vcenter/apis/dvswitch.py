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
parser.add_argument('protocol')    # 设置mtu时钟时间
parser.add_argument('operation')    # 设置mtu时钟时间
parser.add_argument('uplink_quantity')    # 设置mtu时钟时间
parser.add_argument('uplink_prefix')    # 设置mtu时钟时间
parser.add_argument('switch_version')    # 设置mtu时钟时间

parser.add_argument("old_uplink_name")  # 修改前的单个上传链路名称
parser.add_argument("new_uplink_name")  # 修改后的单个上传链路名称



class DVSwitchManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
        TODO 修改error_code
        """
        try:
            g.error_code = 4701
            args = parser.parse_args()
            if not args['platform_id']:
                g.error_code = 4702
                raise RuntimeError('Parameter Error!!!')

            data = get_dvswitch_infos(args['platform_id'])
        except Exception as e:
            return set_return_val(False, {}, str(e), g.error_code), 400

        return set_return_val(True, data, 'Get Dvswitch Info Success!!!', 4700)

    @basic_auth.login_required
    def post(self):
        """
        TODO 创建error_code
        """
        try:
            g.error_code = 4751
            args = parser.parse_args()

            if not all([args['platform_id'], args['switch_name'], args['dc_name']]):
                g.error_code = 4752
                raise RuntimeError('Parameter Error!!!')

            dvsw = DVSwitch(args['platform_id'])
            dvsw.create_dvswitch(args)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        
        return set_return_val(True, [], 'Create Vswitch Success!!!', 4750)

    @basic_auth.login_required
    def delete(self, dvswitch_id):
        """
        TODO 修改error_code
        """
        try:
            g.error_code = 4801
            args = parser.parse_args()

            if not args['platform_id']:
                g.error_code = 4802
                raise RuntimeError('Parameter Error!!!')

            dvsw = DVSwitch(args['platform_id'])
            # dvsw.delete_dvswitch_by_name("test", 'Datacenter')
            dvsw.delete_dvswitch_by_id(dvswitch_id)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400

        return set_return_val(True, [], 'Delete Vswitch Success!!!', 4800)

    @basic_auth.login_required
    def put(self, dvswitch_id):
        """
        TODO 修改error_code
        """
        try:
            g.error_code = 4851
            args = parser.parse_args()
            if not all([args['platform_id'],]):
                g.error_code = 4852
                raise RuntimeError('Parameter Error!!!')

            dvsw = DVSwitch(args['platform_id'])
            dvsw.update_dvswich(dvswitch_id, args)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code)

        return set_return_val(True, {}, 'Update Vswitch Success!!!', 4850)
