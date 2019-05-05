# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base import control
from flask import g

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')

ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': ''
}


class PlatformTypeMg(Resource):
    def get(self):
        """
        查询云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: query
           name: id
           type: integer
           format: int64
         - in: query
           name: name
           type: string
           description: 平台类型名称
       responses:
         200:
           description: 查询云平台类型
           schema:
             id: platform_type
             properties:
               id:
                 type: string
                 description: 类型ID
                 default: 1
               name:
                 type: string
                 description: 类型名称
                 default: vCenter
        """
        args = parser.parse_args()
        try:

            data = control.platform_type.type_list(id=args['id'], name=args['name'])
        except Exception, e:
            return set_return_val(False, [], str(e), 1319), 400

        return set_return_val(True, data, 'Platform type query succeeded.', 1430)

    def post(self):
        """
        根据id更新云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: query
           name: name
           type: string
           description: 平台类型名称
       responses:
         200:
           description: 根据用户id删除云平台类型
           schema:
             id: platform_type
             properties:
               id:
                 type: string
                 description: 类型ID
                 default: 1
               name:
                 type: string
                 description: 类型名称
                 default: vCenter
        """
        args = parser.parse_args()

        if not args['name']:
            raise Exception('Please pass in the platform type name.')

        try:
            control.platform_type.type_create(name=args['name'])

        except Exception as e:
            return set_return_val(False, [], str(e), 1319), 400
        return set_return_val(True, [], 'Platform type create succeeded.', 1430)

    def put(self, id):
        """
        根据id更新云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
         - in: query
           name: name
           type: string
           description: 平台类型名称
       responses:
         200:
           description: 根据用户id删除云平台类型
           schema:
             id: platform_type
             properties:
               id:
                 type: string
                 description: 类型ID
                 default: 1
               name:
                 type: string
                 description: 类型名称
                 default: vCenter
        """

        args = parser.parse_args()
        if not args['name']:
            raise Exception('Please pass in the platform type name.')
        try:
            control.platform_type.type_update(id, args['name'])

        except Exception, e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, [], 'Platform type update succeeded.', 1520)

    def delete(self, id):
        """
        根据id删除云平台类型信息
       ---
       tags:
          - cloudplatformtype
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
           description: 根据用户id删除云平台类型
           schema:
             id: platform_type
             properties:
               id:
                 type: string
                 description: 类型ID
                 default: 1
               name:
                 type: string
                 description: 类型名称
                 default: vCenter
        """
        try:
            control.platform_type.type_delete(id)
        except Exception as e:

            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, [], 'Platform type delete succeeded.', 1520)
