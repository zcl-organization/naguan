# -*- coding:utf-8 -*-
from flask import g
from flask_restful import reqparse, Resource, fields, marshal_with

from app.common.tool import set_return_val
from auth import basic_auth
from app.main.base import control
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 系统配置 请求格式
parser = reqparse.RequestParser()
parser.add_argument('platform_name', type=str)
parser.add_argument('version_information', type=str)
parser.add_argument('copyright', type=str)
parser.add_argument('user_authentication_mode', type=str)
parser.add_argument('debug', type=int)


# 自定义格式，fields.Raw
class LogoForm(fields.Raw):
    def format(self, value):
        return '/static/img/' + value


# 日志存储位置
class StoreForm(fields.Raw):
    def format(self, value):
        return '/static/store_log/' + value


# 获取系统配置参数
system_fields = {
    'platform_name': fields.String,
    'version_information': fields.String,
    'logo': LogoForm(attribute='logo'),  # attribute='模型字段名'
    'copyright': fields.String,
    'user_authentication_mode': fields.String,
    'debug': fields.Integer,
    'STORE_LOG': StoreForm(attribute='store_log'),
}

# 响应 格式
result_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'ok': fields.Boolean,
    'data': fields.Nested(system_fields)
}

# 更新系统配置资源定制格式
sysconfig_fields = {
    'id': fields.Integer,
    'platform_name': fields.String,  # 平台名称
    'version_information': fields.String,  # 版本号
    'copyright': fields.String,  # 版权
    'user_authentication_mode': fields.String,  # 用户验证模式
    'debug': fields.Integer,
    'STORE_LOG': fields.String,  # 日志存储位置
}

result_fields2 = {
    'code': fields.Integer,
    'msg': fields.String,
    'ok': fields.Boolean,
    'data': fields.List(fields.Nested(sysconfig_fields))
}


class System(Resource):
    @basic_auth.login_required
    @marshal_with(result_fields)
    def post(self):
        """
        初始化系统配置
        ---
        tags:
          - system config
        produces:
          - "application/json"
        parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
              - platform_name
              - version_information
              - copyright
              - user_authentication_mode
              - debug
              properties:
                platform_name:
                  type: string
                  default: kstack-naguan
                  description: 平台名称
                  example: kstack-naguan
                version_information:
                  type: string
                  default: 1.0.1
                  description: 版本
                  example: 1.0.1
                copyright:
                  type: string
                  default: 2017-2019
                  description: copyright
                  example: 2017-2019
                user_authentication_mode:
                  type: string
                  default: kstack-naguan
                  description: 登录认证模式
                  example: local
                debug:
                  type: integer
                  default: 1
                  description: debug 模式
                  example: 1
        responses:
          200:
            description: 创建系统配置
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

        if int(args['debug']) not in [1, 2]:
            raise Exception('The debug parameter is wrong, 1 is True and 2 is False')
        try:

            control.system.system_config_create(platform_name=args['platform_name'],
                                                version_information=args['version_information'],
                                                copyright=args['copyright'],
                                                user_authentication_mode=args['user_authentication_mode'],
                                                debug=args['debug'])
        except Exception as e:
            control.event_logs.eventlog_create(type='system', result=False, resources_id='', event=unicode('创建系统配置'),
                                               submitter=g.username)
            return set_return_val(False, [], str(e), 1601), 400
        control.event_logs.eventlog_create(type='system', result=True, resources_id=1, event=unicode('创建系统配置'),
                                           submitter=g.username)
        return set_return_val(True, [], 'System config created successfully', 1600)

    @basic_auth.login_required
    def get(self):
        """
        获取系统配置信息
        ---
        tags:
         - system config
        responses:
          200:
            description: 创建系统配置
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
                      copyright:
                        type: string
                        default: 2019
                        description: copyright
                      debug:
                        type: string
                        default: True
                        description: debug
                      id:
                        type: string
                        default: 1
                        description: id
                      platform_name:
                        type: string
                        default: naguan
                        description: platform_name
                      user_authentication_mode:
                        type: string
                        default: local
                        description: user_authentication_mode
                      version:
                        type: string
                        default: 1.0.1
                        description: version
            """

        try:
            data = control.system.system_config_list()
        except Exception as e:
            return set_return_val(False, [], str(e), 1631), 400
        return set_return_val(True, data, 'System configuration succeeded', 1630)

    @basic_auth.login_required
    @marshal_with(result_fields2)
    def put(self):
        """
        更新系统配置
        ---
        tags:
          - system config
        parameters:
          - in: query
            name: platform_name
            type: string
            description: 平台名称
          - name: version_information
            type: string
            in: query
            description: 版本信息
          - name: copyright
            type: string
            in: query
            description: 版权
          - name: user_authentication_mode
            type: string
            in: query
            description: 用户验证模式
          - name: debug
            type: int
            in: query
            description: debug
        responses:
          200:
            description: 更新系统配置
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
            control.system.system_config_update(platform_name=args['platform_name'],
                                                version_information=args['version_information'],
                                                copyright=args['copyright'],
                                                user_authentication_mode=args['user_authentication_mode'],
                                                debug=args['debug'])

        except Exception as e:
            control.event_logs.eventlog_create(type='system', result=False, resources_id='', event=unicode('更新系统配置'),
                                               submitter=g.username)
            return set_return_val(False, [], str(e), 1611), 400
        control.event_logs.eventlog_create(type='system', result=True, resources_id=1, event=unicode('更新系统配置'),
                                           submitter=g.username)
        return set_return_val(True, [], 'System configuration updated succeeded', 1610)

