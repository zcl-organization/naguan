# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val

from app.main.vcenter.sync import sync_all_new
from app.main.vcenter import control
from app.main.base import control as base_control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class VCenterSyncManage(Resource):

    @basic_auth.login_required
    def post(self):
        """
        同步vCenter tree 信息(New)
        ---
       tags:
          - vCenter tree
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
              - platform_id
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
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
                  type: string
                  items:
                    properties:
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
        args = parser.parse_args()
        data = dict(
            type='vcenter',
            result=False,
            resources_id=None,
            event=unicode('同步vcenter信息'),
            submitter=g.username,
        )
        try:
            g.error_code = 4051
            if not args['platform_id']:
                g.error_code = 4052
                raise Exception('Parameter error')
            sync_all_new(args['platform_id'])
            data['result'] = True
        except Exception as e:
            return set_return_val(False, {}, str(e), g.error_code), 400
        finally:
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, {}, 'Sync vcneter tree success', 4050)
