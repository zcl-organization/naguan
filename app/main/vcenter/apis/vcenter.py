# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.vcenter.control import vcenter as vcenter_manage


parser = reqparse.RequestParser()
parser.add_argument('id')
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
            name: id
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
            print(args)
            vcenter_tree = vcenter_manage.vcenter_tree_list(int(args['id']))
            ret_status['data'] = vcenter_tree
            ret_status['ok'] = True
            ret_status['msg'] = '获取成功'
            ret_status['code'] = '1230'
        except Exception as e:
            ret_status['ok'] = False
            ret_status['msg'] = '获取失败'
            ret_status['code'] = '1239'
            ret_status['data'] = {}
            return ret_status, 400
        return ret_status

    def post(self):
        args = parser.parse_args()
        vcenter_manage.sync_tree(args['id'])
        return 'success'

    def delete(self):
        pass

    def put(self):
        pass
