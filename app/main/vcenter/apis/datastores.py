# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class DataStoreManage(Resource):

    def get(self):
        """
         获取vCenter datastore 信息
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
            description: 获取datastore 成功
            schema:
              properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      capacity:
                        type: string
                        default: 591363309568
                        description: capacity
                      dc_mor_name:
                        type: string
                        default: datacenter-661
                        description: dc_mor_name
                      dc_name:
                        type: string
                        default: 200
                        description: Datacenter
                      ds_mor_name:
                        type: string
                        default: datastore-671
                        description: ds_mor_name
                      ds_name:
                        type: string
                        default: datastore1
                        description: ds_name
                      free_capacity:
                        type: string
                        default: 173924155392
                        description: free_capacity
                      host:
                        type: string
                        default: 192.168.12.203
                        description: host
                      id:
                        type: string
                        default: 200
                        description: id
                      local:
                        type: boolean
                        default: 200
                        description: local
                      platform_id:
                        type: string
                        default: 200
                        description: platform_id
                      ssd:
                        type: boolean
                        default: true
                        description: ssd
                      type:
                        type: string
                        default: VMFS
                        description: type
                      used_capacity:
                        type: string
                        default: 417439154176
                        description: type
                      uuid:
                        type: string
                        default: 5c19f5d5-ada3c960-acd7-b8ca3af5a86b
                        description: type
                      version:
                        type: string
                        default: 6.8.2
                        description: type

          400:
            description: 获取datastore失败
            schema:
              properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
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
            return set_return_val(False, [], str(e), 2441), 400
        return set_return_val(True, data, 'Datastore gets success.', 2440)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
