# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('dc_name')
parser.add_argument('dc_id')


class DataCenterManage(Resource):

    def post(self):
        try:
            args = parser.parse_args()
            data = control.datacenters.create_datacenter(
                platform_id=args.get('platform_id'), dc_name=args.get('dc_name'))
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001)
        return set_return_val(True, data, 'Datastore create success.', 3000)

    def put(self):
        pass

    def delete(self):
        try:
            args = parser.parse_args()
            dc_id = args.get('dc_id')
            control.datacenters.del_datacenter(platform_id=args.get('platform_id'), dc_id=dc_id)
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001)
        return set_return_val(True, {}, 'Datastore delete success.', 3000)


