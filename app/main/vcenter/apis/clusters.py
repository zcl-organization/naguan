# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.base import control as base_control


parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('cluster_id')  # cluster_id 群集id
parser.add_argument('dc_id')
parser.add_argument('cluster_name')
parser.add_argument('dc_name')


class ClustersManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取vCenter DataCenter 信息
        ---
       tags:
          - vCenter Cluster
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
           - in: query
            name: platform_id
            type: integer
            required: false
          - in: query
            name: dc_name
            type: string
            required: false
          - in: query
            name: cluster_id
            type: integer
            required: false
          - in: query
            name: cluster_name
            type: string
            required: false
       responses:
          200:
            description: vCenter Cluster 信息
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
                      name:
                        type: string
                        default: Cluster
                        description: Cluster
                      mor_name:
                        type: string
                        default: Cluster_mor_name
                        description: Cluster_mor_name
                      platform_id:
                        type: integer
                        default: 1
                        description: platform_id
                      dc_name:
                        type: string
                        default: DataCenter
                        description: DataCenter
                      dc_mor_name:
                        type: string
                        default: datacenter-365
                        description: mor_name
                      vm_nums:
                        type: integer
                        default: 1
                        description: vm_nums
                      host_nums:
                        type: integer
                        default: 1
                        description: host_nums
                      cpu_capacity:
                        type: integer
                        default: 0
                        description: cpu_capacity
                      used_cpu:
                        type: integer
                        default: 0
                        description: used_cpu
                      memory:
                        type: integer
                        default: 0
                        description: memory
                      used_memory:
                        type: integer
                        default: 0
                        description: used_memory
                      capacity:
                        type: integer
                        default: 1
                        description: capacity
                      used_capacity:
                        type: integer
                        default: 1
                        description: used_capacity
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
                  default: "Clusters not found"
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            if not args['platform_id']:
                raise Exception('Parameter error')
            data = control.clusters.find_clusters(platform_id=args['platform_id'], cluster_name=args['cluster_name'],
                                                  cluster_id=args['cluster_id'], dc_name=args['dc_name'])
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001), 400
        return set_return_val(True, data, 'Clusters info get success.', 3000)

    @basic_auth.login_required
    def post(self):
        """
         创建Cluster信息
        ---
       tags:
          - vCenter Cluster
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
              - platform_id
              - vm_uuid
              - snapshot_name
              - action
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                dc_id:
                  type: integer
                  default: 1
                  description: 数据中心id
                  example: 1
                cluster_name:
                  type: string
                  default: Cluster
                  description: 集群名
                  example: Cluster
       responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "创建成功"
                data:
                  type: array
                  items:
                    properties:
          400:
            description: 创建失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "创建失败"
                data:
                  type: array
                  items:
                    properties:
        """
        data = dict(
            type='Cluster',
            result=True,
            resources_id=None,
            event=unicode('创建cluster'),
            submitter=g.username,
        )
        try:
            args = parser.parse_args()
            if not all([args['platform_id'], args['dc_id'], args['cluster_name']]):
                raise Exception('Parameter error')
            cluster_id = control.clusters.create_cluster(platform_id=args.get('platform_id'),
                                                         dc_id=args.get('dc_id'), cluster_name=args.get('cluster_name'))
            data['resources_id'] = cluster_id
        except Exception as e:
            data['result'] = False
            return set_return_val(False, data, str(e), 3001)
        finally:
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, data, 'clusters create success.', 3000)

    def put(self):
        pass

    @basic_auth.login_required
    def delete(self, id):
        """
         删除Cluster信息
        ---
       tags:
          - vCenter Cluster
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
              - platform_id
              - vm_uuid
              - snapshot_name
              - action
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
          - in: path
            type: integer
            format: int64
            name: id
            required: true
       responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "删除成功"
                data:
                  type: array
                  items:
                    properties:
          400:
            description: 创建失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "删除失败"
                data:
                  type: array
                  items:
                    properties:
        """
        data = dict(
            type='Cluster',
            result=True,
            resources_id=id,
            event=unicode('删除cluster'),
            submitter=g.username,
        )
        try:
            args = parser.parse_args()
            if not all([args['platform_id'], id]):
                raise Exception('Parameter error')
            control.clusters.del_cluster(args.get('platform_id'), cluster_id=id)
        except Exception as e:
            data['result'] = False
            return set_return_val(False, data, str(e), 3001)
        finally:
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, data, 'cluster delete success.', 3000)
