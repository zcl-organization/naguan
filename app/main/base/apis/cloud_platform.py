# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.control import cloud_platform as platform_manage


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('platform_type_id')
parser.add_argument('platform_name')
parser.add_argument('ip')
parser.add_argument('port')
parser.add_argument('admin_name')
parser.add_argument('admin_password')
parser.add_argument('remarks')


ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': ''
}


class CloudPlatformManage(Resource):
    def get(self):
        """
        获取云平台信息
        ---
        tags:
          - cloudplatform
        parameters:
          - in: query
            name: id
            type: string
          - in: query
            name: platform_type_id
            type: string
          - in: query
            name: platform_name
            type: string
        responses:
          200:
            description: 获取云平台信息
            schema:
              id: User
              properties:
                id:
                  type: string
                  description: 用户id
                  default: Steven Wilson
                  name: code
        """
        args = parser.parse_args()
        try:
            options = {
                'id': args['id'],
                'platform_type_id': args['platform_type_id'],
                'platform_name': args['platform_name'],
            }
            platform_list = platform_manage.platform_list(options)
            ret_status['code'] = '1530'
            ret_status['msg'] = '查询成功'
            ret_status['data'] = platform_list
            ret_status['ok'] = True
            return ret_status
        except Exception, e:
            ret_status['code'] = '1530'
            ret_status['msg'] = '查询异常'
            ret_status['data'] = ''
            ret_status['ok'] = False

        return ret_status, 400

    def post(self):
        """
       新增云平台信息
       ---
       tags:
          - cloudplatform
       parameters:
         - in: formData
           name: platform_type_id
           type: string
           required: true
         - in: formData
           name: platform_name
           type: string
           required: true
         - in: formData
           name: admin_name
           type: string
           required: true
         - in: formData
           name: admin_password
           type: string
           required: true
         - in: formData
           name: port
           type: string
           required: true
         - in: formData
           name: ip
           type: string
           required: true
         - in: formData
           name: remarks
           type: string
           required: true
       responses:
         200:
           description: A single user create item
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """
        args = parser.parse_args()
        try:
            options = {
                'platform_type_id': args['platform_type_id'],
                'platform_name': args['platform_name'],
                'admin_name': args['admin_name'],
                'admin_password': args['admin_password'],
                'port': args['port'],
                'ip': args['ip'],
                'remarks': args['remarks']
            }
            result = platform_manage.platform_create(options)
            if result:
                ret_status['code'] = '1500'
                ret_status['msg'] = '创建成功'
                ret_status['data'] = ''
                ret_status['ok'] = True
                return ret_status
            else:
                ret_status['code'] = '1501'
                ret_status['msg'] = '创建失败'
                ret_status['data'] = ''
                ret_status['ok'] = False
        except Exception, e:
            ret_status['code'] = '1509'
            ret_status['msg'] = '创建失败'
            ret_status['data'] = ''
            ret_status['ok'] = False
        return ret_status, 400

    def put(self, id):
        """
        更新云平台信息
        ---
        tags:
          - cloudplatform
        parameters:
         - in: path
           type: integer
           format: int64
           name: id
           required: true
         - in: formData
           name: admin_name
           type: string
         - name: admin_password
           type: string
           in: formData
         - name: port
           type: string
           in: formData
         - name: remarks
           type: string
           in: formData
        responses:
         200:
           description: 更新云平台信息
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """
        args = parser.parse_args()
        try:
            options = {
                'ip': args['ip'],
                'admin_name': args['admin_name'],
                'admin_password': args['admin_password'],
                'port': args['port'],
                'remarks': args['remarks']
            }
            result = platform_manage.platform_update(id, options)
            if result:
                ret_status['code'] = '1520'
                ret_status['msg'] = '更新成功'
                ret_status['data'] = ''
                ret_status['ok'] = True
                return ret_status
            else:
                ret_status['code'] = '1520'
                ret_status['msg'] = '更新失败'
                ret_status['data'] = ''
                ret_status['ok'] = False
        except Exception, e:
            ret_status['code'] = '1529'
            ret_status['msg'] = '更新异常'
            ret_status['data'] = ''
            ret_status['ok'] = False
        return ret_status, 400

    def delete(self, id):
        """
        根据id删除云平台信息
       ---
       tags:
          - cloudplatform
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
           description: 根据用户id删除用户信息
           schema:
             id: User
             properties:
               id:
                 type: string
                 description: 用户id
                 default: Steven Wilson
        """
        try:
            result = platform_manage.platform_delete(id)
            if result:
                ret_status['code'] = '1510'
                ret_status['msg'] = '删除成功'
                ret_status['data'] = ''
                ret_status['ok'] = True
                return ret_status
            else:
                ret_status['code'] = '1511'
                ret_status['msg'] = '删除失败'
                ret_status['data'] = ''
                ret_status['ok'] = False
        except Exception, e:
            ret_status['code'] = '1519'
            ret_status['msg'] = '删除异常'
            ret_status['data'] = ''
            ret_status['ok'] = False
        return ret_status, 400