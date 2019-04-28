# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter.control import network_port_group as network_manage
parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class NetworkPortGroupManage(Resource):

    def get(self):

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



