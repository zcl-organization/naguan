# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.base import control as base_control
from app.main.base import task

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class VCenterManage(Resource):
    def get(self):
        """
         获取vCenter tree 信息
        ---
        tags:
          - vCenter tree
        parameters:
          - in: query
            name: platform_id
            type: string
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
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 1
                      type:
                        type: string
                      platform_id:
                        type: string
                      dc_host_folder_mor_name:
                        type: string
                      dc_mor_name:
                        type: string
                      dc_oc_name:
                        type: string
                      cluster_mor_name:
                        type: string
                      cluster_oc_name:
                        type: string
                      mor_name:
                        type: string
                      name:
                        type: string
                      dc_vm_folder_mor_name:
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
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """
        # parser.add_argument('id')
        args = parser.parse_args()
        try:
            if not args['platform_id']:
                raise Exception('Parameter error')
            data = control.vcenter.vcenter_tree_list(int(args['platform_id']))

        except Exception as e:
            return set_return_val(False, {}, 'Failed to get vcneter tree', 1239), 400
        return set_return_val(True, data, 'Get vcneter tree success', 1230)

    def post(self):
        """
        同步vCenter tree 信息
        ---
        tags:
          - vCenter tree
        parameters:
          - in: query
            name: platform_id
            type: string
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
                data:
                  type: string
                  items:
                    properties:
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
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        try:

            if not args['platform_id']:
                raise Exception('Parameter error')
            # control.vcenter.sync_tree(args['platform_id'])
            task = control.vcenter.sync_tree.apply_async(args=[args['platform_id']], queue='vsphere')
            print(dir(task))
            base_control.task_logs.create_log(task.task_id, 'wait', 'vsphere', 'sync_tree')
        except Exception as e:
            return set_return_val(False, {}, 'Failed to sync vcneter tree', 1239), 400

        return set_return_val(True, {}, 'Sync vcneter tree success', 1239)
