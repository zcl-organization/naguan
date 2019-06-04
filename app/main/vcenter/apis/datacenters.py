# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control


parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('dc_name')


class DataCenterManage(Resource):

    # @basic_auth.login_required
    # def get(self):
    #     """
    #      获取vCenter center 信息
    #     ---
    #     """
    #     args = parser.parse_args()
    #     # test_get_ds(args['platform_id'])
    #     try:
    #         if not args['platform_id']:
    #             raise Exception('Parameter error')
    #         data = control.datastores.get_datastore_by_platform_id(args['platform_id'])
    #     except Exception as e:
    #         return set_return_val(False, [], str(e), 2441), 400
    #     return set_return_val(True, data, 'Datastore gets success.', 2440)

    def post(self):
        try:
            args = parser.parse_args()
            data = control.datacenters.create_datacenter(platform_id=args.get('platform_id'), dc_name=args.get('dc_name'))
                # control.datacenters.create_cluster(datacenter=dc, cluster_name=args.get('c_name'))
        except Exception as e:
            return set_return_val(False, {}, 'Datacenter create fail.', 3001)
        return set_return_val(True, data, 'Datastore create success.', 3000)

    def put(self):
        pass

    def delete(self):
        pass
