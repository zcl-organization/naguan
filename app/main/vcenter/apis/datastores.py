# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class DataStoreManage(Resource):

    def get(self):
        """
         获取vCenter vm_disk 信息
        ---
        tags:
          - vCenter DataStore
        parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
        responses:
          200:
            description: vCenter disk 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: status
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      label:
                        type: string
                      disk_size:
                        type: string
                      disk_file:
                        type: string
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
