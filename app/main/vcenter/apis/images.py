# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('image_id')
parser.add_argument('name')
parser.add_argument('ds_name')


class ImageManage(Resource):
    def get(self):
        """
         获取 images 信息
        ---
        tags:
          - vCenter images
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
                      id:
                        type: string
                        default: 1
                      MorName:
                        type: string
                      OcName:
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
        args = parser.parse_args()
        # id = args.get('id')
        # name = args.get('name')
        # ds_name = args.get('ds_name')

        try:
            data = control.images.images_list(image_id=args['image_id'], name=args['name'], ds_name=args['ds_name'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'image gets success.', 1520)