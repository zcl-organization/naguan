# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.base.apis.auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('image_id')
parser.add_argument('name')
parser.add_argument('ds_name')
parser.add_argument('pgnum')


class ImageManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取 images 信息
        ---
       tags:
          - vCenter images
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: image_id
            type: string
          - in: query
            name: name
            type: string
          - in: query
            name: ds_name
            type: string
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
                      ds_mor_name:
                        type: string
                        default: 1
                        description: ds_mor_name
                      ds_name:
                        type: string
                        default: 1
                        description: ds_name
                      file_type:
                        type: string
                        default: 1
                        description: file_type
                      id:
                        type: string
                        default: 1
                        description: id
                      iso_name:
                        type: string
                        default: 1
                        description: iso_name
                      last_change_time:
                        type: string
                        default: 1
                        description: last_change_time
                      path:
                        type: string
                        default: 1
                        description: path
                      size:
                        type: string
                        default: 1
                        description: size
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
            pgnum = args['pgnum'] if args['pgnum'] else 1
            data, pg = control.images.images_list(image_id=args['image_id'], name=args['name'], ds_name=args['ds_name'],
                                                  pgnum=pgnum)
        except Exception as e:
            return set_return_val(False, [], str(e), 2451), 400
        return set_return_val(True, data, 'image gets success.', 2450, pg)
