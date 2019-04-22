# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.control.role import role_list_c, role_create_c, role_update_c, role_delete_c

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('pgnum', type=int)
parser.add_argument('description', type=str)


class RoleManage(Resource):

    def get(self):
        """
         获取角色信息
         ---
         tags:
           - role
         summary: Add a new pet to the store
         parameters:
           - in: query
             name: name
             type: string
             description: 角色名
           - in: query
             name: pgnum
             type: string
             description: 页码
         responses:
           200:
             description: 获取角色信息
             schema:
               id: Role
               properties:
                 name:
                   type: string
                   description: The name of the user
                   default: Steven Wilson
         """
        args = parser.parse_args()
        name = args.get('name')
        pgnum = args.get('pgnum')
        if not pgnum:  # 默认第一页
            pgnum = 1
        options = {
            'name': name,
            'pgnum': pgnum
        }
        role, pg = role_list_c(options)
        response_data = {
            'code': 1200,
            'ok': True,
            'data': role,
            'msg': '获取角色信息成功',
            'pg': pg,
        }
        return response_data

    def post(self):
        """
         创建角色信息
         ---
         tags:
           - role
         summary: Add a new pet to the store
         parameters:
           - in: query
             name: name
             type: string
             description: 角色名
           - in: query
             name: description
             type: string
             description: 描述
         responses:
           200:
             description: 创建角色信息
             schema:
               id: Role
               properties:
                 name:
                   type: string
                   description: The name of the user
                   default: Steven Wilson
         """
        args = parser.parse_args()
        name = args.get('name')
        description = args.get('description')
        options = {
            'name': name,
            'description': description,
        }
        role = role_create_c(options)
        if role:
            response_data = {
                'code': 3000,
                'ok': True,
                'data': role,
                'msg': '创建角色信息成功',
            }
            return response_data
        else:
            response_data = {
                'code': 3001,
                'ok': False,
                'data': '',
                'msg': '角色名已存在',
            }
            return response_data

    def put(self, id=None):
        """
         更新角色信息
         ---
         tags:
           - role
         parameters:
           - in: path
             type: integer
             format: int64
             name: id
             required: true
           - in: query
             name: name
             type: string
             description: 角色名
           - in: query
             name: description
             type: string
             description: 描述
         responses:
           200:
             description: 更新角色名和描述
             schema:
               id: Role
               properties:
                 name:
                   type: string
                   description: The name of the user
                   default: Steven Wilson
         """
        args = parser.parse_args()
        name = args.get('name')
        description = args.get('description')
        options = {
            'id': id,
            'name': name,
            'description': description,
        }
        if role_update_c(options):
            response_data = {
                'code': 3000,
                'ok': True,
                'data': options,
                'msg': '更改角色信息成功',
            }
            return response_data
        else:
            response_data = {
                'code': 3001,
                'ok': False,
                'data': '',
                'msg': '更改角色信息失败',
            }
            return response_data

    def delete(self, id=None):
        """
        删除角色信息
        ---
        tags:
          - role
        parameters:
          - in: path
            type: integer
            format: int64
            name: id
            required: true
        responses:
          200:
            description: 删除角色
            schema:
              id: Role
              properties:
                name:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
          """
        name = role_delete_c(id)
        if name:
            response_data = {
                'code': 3000,
                'ok': True,
                'data': '被删除角色名：' + name,
                'msg': '删除角色信息成功',
            }
            return response_data
        else:
            response_data = {
                'code': 3001,
                'ok': False,
                'data': '',
                'msg': '删除角色信息失败',
            }
            return response_data

