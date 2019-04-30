# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter.control import vcenter as vcenter_manage

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
ret_status = {
    'ok': True,
    'msg': '',
    'code': '200',
    'data': {}
}


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
            data = vcenter_manage.vcenter_tree_list(int(args['platform_id']))

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
            # vcenter_manage.sync_tree(args['platform_id'])
            vcenter_manage.sync_tree.apply_async(args=[args['platform_id']])
        except Exception as e:
            return set_return_val(False, {}, 'Failed to sync vcneter tree', 1239), 400

        return set_return_val(True, {}, 'Sync vcneter tree success', 1239), 400

    def delete(self):
        pass

    def put(self):
        pass
