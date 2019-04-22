# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.control import platform_type as platform_type_manage
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
            options = {
                'id': args['id'],
                'name': args['name'],
            }
            result = platform_type_manage.platform_type_list(options)
            ret_status['data'] = result
            ret_status['code'] = 1430
            ret_status['ok'] = True
            ret_status['msg'] = '查询成功'

            return ret_status
        except Exception, e:
            ret_status['data'] = ''
            ret_status['code'] = 1439
            ret_status['ok'] = False
            ret_status['msg'] = '查询异常'
            return ret_status, 400

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
        try:
            if args['name']:
                options = {
                    'name': args['name']
                }
            else:
                ret_status['code'] = 1402
                raise Exception('请传入平台类型名称.')
            result = platform_type_manage.platform_type_create(options)
            if result:
                ret_status['code'] = 1400
                ret_status['msg'] = '创建成功'
                ret_status['ok'] = True
                ret_status['data'] = result
            else:
                ret_status['code'] = 1401
                raise Exception('创建失败.')

        except Exception, e:
            # print()
            ret_status['msg'] = str(e)
            ret_status['ok'] = False
            return ret_status, 400
        return result

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
        print('id:', id)
        args = parser.parse_args()
        try:
            options = {
                'name': args['name'],
            }
            result = platform_type_manage.platform_type_update(id, options)
            if result:
                ret_status['code'] = '1520'
                ret_status['msg'] = '更新成功'
                ret_status['data'] = ''
                ret_status['ok'] = True
                return ret_status
            else:

                raise Exception('update failed')
        except Exception, e:
            ret_status['data'] = ''
            ret_status['ok'] = False
            ret_status['msg'] = str(e)
            ret_status['code'] = 1529
            return ret_status, 400
        return ret_status

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
            result = platform_type_manage.platform_type_delete(id)
            if result:
                ret_status['code'] = '1510'
                ret_status['msg'] = '删除成功'
                ret_status['data'] = ''
                ret_status['ok'] = True
            else:
                ret_status['code'] = '1511'
                raise Exception('删除失败', id)
        except Exception as e:
            # print(e)
            ret_status['msg'] = str(e)
            ret_status['data'] = ''
            ret_status['ok'] = False
            return ret_status, 400
        return ret_status
