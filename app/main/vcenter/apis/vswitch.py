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
    def delete(self, vswiter_id):
        try:
            args = parser.parse_args()

            if not args['platform_id']:
                raise RuntimeError('Parameter Error!!!')

            vsw = VSwitch(args['platform_id'])
            vsw.delete_vswitch_by_id(vswiter_id)
        except Exception as e:
            return set_return_val(False, [], str(e), 3005), 400

        return set_return_val(True, [], 'Delete Vswitch Success!!!', 3004)

    @basic_auth.login_required
    def put(self, vswiter_id):
        try:
            args = parser.parse_args()
            if not all([args['host_name'], args['switch_name']]):
                raise RuntimeError('Parameter Error!!!')

            vsw = VSwitch(args['platform_id'])
            vsw.update_vswich(vswiter_id, args)
        except Exception as e:
            return set_return_val(False, [], str(e), 3007)

        return set_return_val(True, {}, 'Update Vswitch Success!!!', 3006)
