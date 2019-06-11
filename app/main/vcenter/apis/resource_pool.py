# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.base.apis.auth import basic_auth
from app.main.vcenter.control.resource_pool import check_if_resource_pool_exists
from app.main.vcenter.control.resource_pool import ResourcePool

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('dc_mor_name')
parser.add_argument('cluster_mor_name')
# parser.add_argument('resource_pool_id')   # 删除时的资源池id
parser.add_argument('cluster_name')  #  创建或是删除资源池所在的集群位置
parser.add_argument('dc_name')  # 归属的数据中心名称
parser.add_argument('rp_name')  # 要创建或是删除的资源池名称
parser.add_argument('root_rp_name')  # 创建资源池归属的根项
parser.add_argument('data_args')   # 创建资源池使用的参数字典


class ResourcePoolManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
         获取vCenter resource pool 信息
        ---
       tags:
          - vCenter ResourcePool
       security:
       - basicAuth:
          type: http
          scheme: basic
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
            return set_return_val(False, [], str(e), 2471), 400
        return set_return_val(True, data, 'Datastore gets success.', 2470)

    @basic_auth.login_required
    def post(self):
        """
        1. 判断数据库中是否存在
        2. 创建创建操作
        3. 异常处理
        """
        args = parser.parse_args()

        try:
            if not all([args['platform_id'], args['cluster_name'], args['rp_name'], args['dc_name']]):
                raise RuntimeError('Parameter Error!!!')

            if check_if_resource_pool_exists(
                dc_name=args['dc_name'], cluster_name=args['cluster_name'], resource_pool_name=args['rp_name']):
                raise RuntimeError('This ResourcePool Exists')

            rp = ResourcePool(args['platform_id'])
            data_args = {} if not args['data_args'] else args['data_args']
            rp.create_pool(args['cluster_name'], args['rp_name'], args['root_rp_name'], **data_args)
        except Exception as e:
            return set_return_val(False, {}, str(e), 2551), 400

        return set_return_val(True, {}, 'ResourcePool Create Success', 2550)

    @basic_auth.login_required
    def delete(self, resource_pool_id):
        args = parser.parse_args()

        try:
            if not args['platform_id']:
                raise RuntimeError('Parameter Error!!!')

            if not check_if_resource_pool_exists(resouce_pool_id=resource_pool_id):
                raise RuntimeError('This ResourcePool Not Exists')

            rp = ResourcePool(args['platform_id'])
            # rp.delete_pool(args['cluster_name'], args['rp_name'])
            rp.delete_pool_by_id(resource_pool_id)
        except Exception as e:
            return set_return_val(False, {}, str(e), 2553), 400

        return set_return_val(True, {}, 'ResourcePool Delete Success', 2552)
