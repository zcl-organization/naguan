# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from app.main.vcenter.control import network_port_group as network_manage
parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class NetworkPortGroupManage(Resource):

    def get(self):
        args = parser.parse_args()
        network_manage.get_network_list(args['platform_id'])
        return 'success'

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



