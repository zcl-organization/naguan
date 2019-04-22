# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse


class ImageManage(Resource):
    def get(self):
        """
         获取 images 信息
        ---
        tags:
          - images
        parameters:
          - in: query
            name: id
            type: string
          - in: query
            name: name
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
        pass

