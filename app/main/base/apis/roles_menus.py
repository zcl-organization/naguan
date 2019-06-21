# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base import control
from auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('role_id')
parser.add_argument('menu_id')


class RolesMenusManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
        获取角色菜单信息
        ---
       tags:
           - role_menu
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: role_id
            type: string
       responses:
          200:
            description: 获取角色菜单信息
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
                      icon:
                        type: string
                        default: icon
                      id:
                        type: string
                        default: icon
                      identifier:
                        type: string
                        default: icon
                      name:
                        type: string
                        default: icon
                      url:
                        type: string
                        default: icon
                      menus:
                        type: array
                        items:
                          properties:
                            icon:
                              type: string
                              default: icon
                            id:
                              type: string
                              default: icon
                            identifier:
                              type: string
                              default: icon
                            name:
                              type: string
                              default: icon
                            url:
                              type: string
                              default: icon
                            menus:
                              type: array
                              items:
                                properties:
                            permission:
                              default: true
                              type: string
        """
        args = parser.parse_args()

        try:
            g.error_code = 1311
            if not args['role_id']:
                g.error_code = 1312
                raise Exception('Parameter error')

            data = control.roles_menus.get_menu_by_role_id(args['role_id'])
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400

        return set_return_val(True, data, 'get role menu successfully', 1310)

    @basic_auth.login_required
    def post(self):
        """
        角色分配菜单权限
        ---
       tags:
           - role_menu
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
              - role_id
              - menu_id
              properties:
                role_id:
                  type: integer
                  default: 1
                  description: 角色id
                  example: 1
                menu_id:
                  type: string
                  default: [1,2]
                  description: 菜单id
                  example: '[1,2]'
       responses:
          200:
            description: 分配菜单权限
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
            g.error_code = 1341
            if not all([args['role_id'], args['menu_id']]):
                g.error_code = 1342
                raise Exception('Parameter error')
            control.roles_menus.update_role(role_id=args['role_id'], menu_id=args['menu_id'])
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400

        return set_return_val(True, [], 'post role menu successfully', 1340)

    @basic_auth.login_required
    def put(self, role_id):
        """
        角色更新菜单权限
        ---
       tags:
           - role_menu
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: role_id
           type: integer
           format: int64
           required: true
           default: 1
         - in: query
           name: menu_id
           type: string
           required: true
           default: '[1,2]'
       responses:
          200:
            description: 分配菜单权限
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
            g.error_code = 1371
            if not args['menu_id']:
                g.error_code = 1372
                raise Exception('Parameter error')
            control.roles_menus.update_role(role_id=role_id, menu_id=args['menu_id'])
        except Exception as e:
            return set_return_val(False, [], 'update role menu failed', g.error_code)
        return set_return_val(True, [], 'update role menu successfully', 1370)

    @basic_auth.login_required
    def delete(self, role_id):
        """
        角色删除菜单权限
        ---
       tags:
           - role_menu
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: role_id
           type: integer
           format: int64
           required: true
           default: 1
       responses:
          200:
            description: 分配菜单权限
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
            control.roles_menus.delete_role(role_id=role_id)
        except Exception as e:
            return set_return_val(False, [], str(e), 1401), 400
        return set_return_val(True, [], 'delete role menu successfully', 1400)
