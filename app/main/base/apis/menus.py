# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse


from app.main.base.control import menu as menu_manage
from app.main.base.control import event_logs
from auth import basic_auth
from flask import g
from flask_security import roles_accepted,current_user
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
    # @basic_auth.login_required
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
            description: 菜单获取
            schema:
              id: User
              properties:
                id:
                  type: string
                  description: 用户id
                  default: Steven Wilson
                  name: code
        """
        print('role:', current_user.is_active)
        try:
            # g.event_request_id =
            # g.event_request_id = get_event_request_id()
            args = parser.parse_args()
            # if not args['pgnum']:
            #     pgnum = 1
            # else:
            #     pgnum = int(args['pgnum'])
            #
            #
            # if not args['pgsize']:
            #     limit = 10
            # else:
            #     limit = int(args['pgsize'])

            options = {
                'id': args['id'],
                'url': args['url'],
                'name': args['name'],
                'identifier': args['identifier'],
                'all': args['all']
            }

            # result, pg = menu_manage.menu_list(options=options)
            result = menu_manage.menu_list(options=options)

            ret_status['data'] = result
            ret_status['msg'] = '获取菜单成功'
            ret_status['code'] = 1310
            ret_status['ok'] = True
            # ret_status['pg'] = pg
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = '获取菜单异常'
            ret_status['code'] = 1319
            ret_status['ok'] = False

        event_options = {
            'type': 'menu',
            'result': ret_status['ok'],
            'resources_id': '',
            'event': unicode('获取菜单信息'),
            'submitter': g.username,
        }
        event_logs.eventlog_create(event_options)
        return ret_status

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
            description: 菜单获取
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

        # 验证is_hide合法性
        if int(args['is_hide']) not in [1, 2]:
            ret_status['code'] = 1104
            ret_status['msg'] = 'is_hide信息不对，请传入正确参数，1为True，2为False'
            ret_status['ok'] = False
            return ret_status
        # 验证 is_hide_children 合法性
        if int(args['is_hide']) not in [1, 2]:
            ret_status['code'] = 1104
            ret_status['msg'] = 'is_hide_children 信息不对，请传入正确参数，1为True，2为False'
            ret_status['ok'] = False
            return ret_status

        options = {
            'icon': args['icon'],
            'url': args['url'],
            'name': args['name'],
            'identifier': args['identifier'],
            'is_hide': int(args['is_hide']),
            'is_hide_children': int(args['is_hide_children']),
            'important': args['important'],
            'parent_id': args['parent_id'],
        }

        try:

            result = menu_manage.menu_create(options=options)
            ret_status['data'] = result
            ret_status['msg'] = '创建菜单成功'
            ret_status['code'] = 1300
            ret_status['ok'] = True
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = '创建菜单异常，请提交正确的参数'
            ret_status['code'] = 1309
            ret_status['ok'] = False

        return ret_status

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
           description: A single user item
           schema:
             id: User
             properties:
               id:
                 type: string
                 description: 用户id
                 default: Steven Wilson
        """
        result = menu_manage.menu_delete(id=id)
        if result:
            result2 = menu_manage.children_menu(id=id)
            if result2:
                ret_status['data'] = ''
                ret_status['msg'] = '当前菜单存在子菜单，请先删除子菜单'
                ret_status['code'] = 1309
                ret_status['ok'] = False
            else:
                ret_status['data'] = ''
                ret_status['msg'] = '删除菜单成功'
                ret_status['code'] = 1300
                ret_status['ok'] = True
        else:
            ret_status['data'] = ''
            ret_status['msg'] = '无法获取到菜单'
            ret_status['code'] = 1309
            ret_status['ok'] = False
        if ret_status['code'] != 1300:
            return ret_status, 300
        else:
            return ret_status

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
           description: 更新菜单信息
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """
        args = parser.parse_args()

        # 验证 is_hide 合法性
        if not args['is_hide']:
            ret_status['code'] = 1104
            raise Exception('请传入 is_hide 信息，1为True，2为False')
        else:
            if int(args['is_hide']) not in [1, 2]:
                ret_status['code'] = 1104
                raise Exception('is_hide 信息不对，请传入正确参数，1为True，2为False')

        try:
            options = {
                'icon': args['icon'],
                'name': args['name'],
                'url': args['url'],
                'identifier': args['identifier'],
                'is_hide': int(args['is_hide']),
                'is_hide_children': int(args['is_hide_children']),
                'parent_id': args['parent_id'],
                'important': args['important'],
            }
            result = menu_manage.menu_update(id, options=options)
            if result:
                ret_status['data'] = ''
                ret_status['msg'] = '更新菜单成功'
                ret_status['code'] = 1320
                ret_status['ok'] = True
            else:
                ret_status['code'] = 1328
                raise Exception('不存在当前菜单')
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = str(e)
            ret_status['ok'] = False
            return ret_status, 400
        return ret_status
