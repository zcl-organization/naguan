# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.main.vcenter.control.datastores import test_get_ds

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class DataStoreManage(Resource):

    def get(self):
        args = parser.parse_args()
        test_get_ds(args['platform_id'])
        return 'test datastore info'

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
