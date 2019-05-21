# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('dc_mor_name')
parser.add_argument('cluster_mor_name')


class ResourcePoolManage(Resource):
    def get(self):
        """
         获取vCenter resource pool 信息
        ---
        tags:
          - vCenter ResourcePool
        parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
          - in: query
            name: dc_mor_name
            type: string
          - in: query
            name: cluster_mor_name
            type: string
        responses:
          200:
            description: vCenter resource pool 信息
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
                      cluster_mor_name:
                        type: string
                        default: domain-c666
                        description: cluster_mor_name
                      cluster_name:
                        type: string
                        default: gat
                        description: cluster_name
                      cpu_expand_able_reservation:
                        type: string
                        default: 1
                        description: cpu_expand_able_reservation
                      cpu_level:
                        type: string
                        default: 4000
                        description: cpu_level
                      cpu_limit:
                        type: string
                        default: 35932
                        description: cpu_limit
                      cpu_max_usage:
                        type: string
                        default: 35932
                        description: cpu_max_usage
                      cpu_over_all_usage:
                        type: string
                        default: 532
                        description: cpu_over_all_usage
                      cpu_reservation:
                        type: string
                        default: 35932
                        description: cpu_reservation
                      cpu_shares:
                        type: string
                        default: 4000
                        description: cpu_shares
                      dc_mor_name:
                        type: string
                        default: datacenter-661
                        description: dc_mor_name
                      dc_name:
                        type: string
                        default: Datacenter
                        description: dc_name
                      id:
                        type: string
                        default: 1
                        description: id
                      memory_expand_able_reservation:
                        type: string
                        default: 1
                        description: memory_expand_able_reservation
                      memory_level:
                        type: string
                        default: normal
                        description: memory_level
                      memory_limit:
                        type: string
                        default: 121616
                        description: memory_limit
                      memory_max_usage:
                        type: string
                        default: 127527813120
                        description: memory_max_usage
                      memory_over_all_usage:
                        type: string
                        default: 37671141376
                        description: memory_over_all_usage
                      memory_reservation:
                        type: string
                        default: 121616
                        description: memory_reservation
                      memory_shares:
                        type: string
                        default: 163840
                        description: memory_shares
                      mor_name:
                        type: string
                        default: resgroup-667
                        description: mor_name
                      name:
                        type: string
                        default: Resources
                        description: name
                      over_all_status:
                        type: string
                        default: green
                        description: over_all_status
                      parent_name:
                        type: string
                        default: gat
                        description: parent_name
                      platform_id:
                        type: string
                        default: 1
                        description: platform_id
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

        try:
            if not args['platform_id']:
                raise Exception('Parameter error')

            data = control.resource_pool.get_resource_pool_list(platform_id=args['platform_id'],
                                                                dc_mor_name=args['dc_mor_name'],
                                                                cluster_mor_name=args['cluster_mor_name'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'Datastore gets success.', 1520)
