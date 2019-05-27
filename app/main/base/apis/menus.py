# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base.control import menu as menu_manage
from app.main.base.control import event_logs

from app.main.base import control
from auth import basic_auth
from flask import g
from flask_security import roles_accepted, current_user

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('icon')
parser.add_argument('url')
parser.add_argument('name')
parser.add_argument('identifier')
parser.add_argument('is_hide')
parser.add_argument('is_hide_children')
parser.add_argument('important')
parser.add_argument('parent_id')
parser.add_argument('pgnum')
parser.add_argument('pgsize')
parser.add_argument('all')

ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': ''
}


class MenuManage(Resource):
    # @roles_accepted('admin', 'user')
    @basic_auth.login_required
    def get(self):
        """
        获取菜单信息
        ---
        tags:
          - menu
        parameters:
          - in: query
            name: id
            type: string
          - in: query
            name: url
            type: string
          - in: query
            name: name
            type: string
          - in: query
            name: identifier
            type: string
          - in: query
            name: all
            type: string
        responses:
          200:
            description: 用户登录
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
        """
        # print('role:', current_user.is_active)
        try:
            args = parser.parse_args()

            data = control.menu.menu_list(menu_id=args['id'], url=args['url'], name=args['name'],
                                          identifier=args['identifier'], all=args['all'])

        except Exception, e:
            return set_return_val(False, [], str(e), 1319), 400
        # event_options = {
        #     'type': 'menu',
        #     'result': ret_status['ok'],
        #     'resources_id': '',
        #     'event': unicode('获取菜单信息'),
        #     'submitter': g.username,
        # }
        # control.event_logs.eventlog_create(type='menu', result=True, resources_id='menu_id', event=unicode('获取菜单信息'),
        #                                    submitter=g.username)
        return set_return_val(True, data, 'Get menu success', 1310)

    @basic_auth.login_required
    def post(self):
        """
        提交新的菜单
        ---
        tags:
          - menu
        parameters:
          - in: formData
            name: icon
            type: string
          - in: formData
            name: url
            type: string
          - in: formData
            name: name
            type: string
          - in: formData
            name: identifier
            type: string
          - in: formData
            name: is_hide
            type: integer
            format: int64
          - in: formData
            name: is_hide_children
            type: integer
            format: int64
          - in: formData
            name: important
            type: string
          - in: formData
            name: parent_id
            type: string
        responses:
          200:
            description: 删除菜单信息
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
            # 验证is_hide合法性
            if int(args['is_hide']) not in [1, 2]:
                raise Exception('is_hide information is incorrect, 1 is True, 2 is False')

            # 验证 is_hide_children 合法性
            if int(args['is_hide_children']) not in [1, 2]:
                raise Exception('is_hide_children information is incorrect, 1 is True, 2 is False')

            id = control.menu.menu_create(icon=args['icon'], url=args['url'], name=args['name'],
                                          identifier=args['identifier'], is_hide=int(args['is_hide']),
                                          is_hide_children=int(args['is_hide_children']), important=args['important'],
                                          parent_id=args['parent_id'])

        except Exception, e:
            control.event_logs.eventlog_create(type='menu', result=False, resources_id='',
                                               event=unicode('创建菜单:%s' % args['name']), submitter=g.username)
            return set_return_val(False, [], str(e), 1319), 400
        control.event_logs.eventlog_create(type='menu', result=True, resources_id=id,
                                           event=unicode('创建菜单:%s' % args['name']), submitter=g.username)
        return set_return_val(True, [], 'Create menu successfully', 1300)

    @basic_auth.login_required
    def delete(self, id):
        """
        根据ID删除菜单信息
       ---
       tags:
          - menu
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
            description: 删除菜单信息
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
            name = control.menu.menu_delete(id=id)
        except Exception as e:
            control.event_logs.eventlog_create(type='menu', result=False, resources_id=id,
                                               event=unicode('删除菜单信息'), submitter=g.username)
            return set_return_val(False, [], str(e), 1319), 400
        control.event_logs.eventlog_create(type='menu', result=True, resources_id=id, event=unicode('删除菜单:%s' % name),
                                           submitter=g.username)
        return set_return_val(False, [], 'Menu deletion successfully', 1300)

    @basic_auth.login_required
    def put(self, id):
        """
        更新菜单信息
        ---
        tags:
          - menu
        parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
         - in: formData
           name: icon
           type: string
         - name: name
           type: string
           in: formData
         - name: url
           type: string
           in: formData
         - name: identifier
           type: string
           in: formData
         - name: is_hide
           type: integer
           format: int64
           in: formData
         - name: is_hide_children
           type: integer
           format: int64
           in: formData
         - name: parent_id
           type: string
           in: formData
         - name: important
           type: string
           in: formData
        responses:
         200:
            description: 删除菜单信息
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
            # 验证 is_hide 合法性
            if not args['is_hide']:
                raise Exception('is_hide information is incorrect, 1 is True, 2 is False')
            else:
                if int(args['is_hide']) not in [1, 2]:
                    raise Exception('is_hide information is incorrect, 1 is True, 2 is False')

            name = control.menu.menu_update(id=id, icon=args['icon'], name=args['name'], url=args['url'],
                                            identifier=args['identifier'], is_hide=int(args['is_hide']),
                                            is_hide_children=int(args['is_hide_children']),
                                            parent_id=args['parent_id'], important=args['important'])

        except Exception, e:
            control.event_logs.eventlog_create(type='menu', result=False, resources_id=id,
                                               event=unicode('更新菜单信息'), submitter=g.username)
            return set_return_val(False, [], str(e), 1319), 400
        control.event_logs.eventlog_create(type='menu', result=True, resources_id=id, event=unicode('更新菜单:%s' % name),
                                           submitter=g.username)
        return set_return_val(True, [], 'Update menu successfully', 1300)
