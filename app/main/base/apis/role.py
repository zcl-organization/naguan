# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base.control.role import role_list, role_create, role_update, role_delete
from app.main.base import control

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
             properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 200
                        description: id
                      name:
                        default: admin
                        type: string
                        description: name
                      description:
                        default: admin
                        type: string
                        description: admin
         """
        args = parser.parse_args()

        if not args['pgnum']:
            pgnum = 1
        else:
            pgnum = args['pgnum']
        try:
            data, pg = control.role.role_list(name=args['name'], pgnum=pgnum)

        except Exception as e:
            return set_return_val(False, [], str(e), 1319), 400

        return set_return_val(True, data, 'Get the role information successfully', 1200, pg)

    def post(self):
        """
         创建角色信息
         ---
         tags:
           - role
         summary: 创建角色信息
         produces:
           - "application/json"
         parameters:
           - in: body
             name: body
             required: true
             schema:
               required:
               - name
               properties:
                  name:
                    type: string
                    default: admin
                    description: 角色名称
                    example: admin
                  description:
                    type: string
                    default: admin
                    description: 角色信息描述
                    example: admin角色
         responses:
           200:
            description: 创建角色信息
            schema:
             properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
         """
        args = parser.parse_args()

        if not all([args['name'], args['description']]):
            raise Exception('Parameter error')
        try:
            control.role.role_create(name=args['name'], description=args['description'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1319), 400

        return set_return_val(True, [], 'The role information is created successfully.', 1200)

    def put(self, id):
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
            description: 更新角色信息
            schema:
             properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
         """
        args = parser.parse_args()
        try:
            control.role.role_update(role_id=int(id), name=args['name'], description=args['description'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1319), 400
        return set_return_val(True, [], 'Role information updated successfully', 1200)

    def delete(self, id):
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
            description: 删除角色信息
            schema:
             properties:
                ok:
                  type: boolean
                  default: 200
                  description: 状态
                code:
                  type: string
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
          """
        try:
            control.role.role_delete(id)
        except Exception as e:
            return set_return_val(False, [], str(e), 1319), 400
        return set_return_val(True, [], 'The role information was deleted successfully.', 1200)
