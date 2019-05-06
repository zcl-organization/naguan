# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class DataStoreManage(Resource):

    def get(self):
        args = parser.parse_args()
        # test_get_ds(args['platform_id'])
        try:
            if not args['platform_id']:
                raise Exception('Parameter error')
            data = control.datastores.get_datastore_by_platform_id(args['platform_id'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'Datastore gets success.', 1520)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
