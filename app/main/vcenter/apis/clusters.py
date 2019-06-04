# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control


parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('c_name')  # cluster_name 群集名
parser.add_argument('dc_id')


class ClustersManage(Resource):
    def post(self):
        try:
            args = parser.parse_args()

            data = control.clusters.create_cluster(args.get('platform_id'),
                                                   dc_id=args.get('dc_id'), cluster_name=args.get('c_name'))
        except Exception as e:
            return set_return_val(False, {}, 'clusters create fail.', 3001)
        return set_return_val(True, data, 'clusters create success.', 3000)

    def put(self):
        pass

    def delete(self):
        try:
            args = parser.parse_args()

            data = control.clusters.del_cluster(args.get('platform_id'),
                                                dc_id=args.get('dc_id'), cluster_name=args.get('c_name'))
        except Exception as e:
            return set_return_val(False, {}, 'clusters create fail.', 3001)
        return set_return_val(True, data, 'clusters create success.', 3000)
