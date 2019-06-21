# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app.common.tool import set_return_val
from app.main.vcenter import control
from app.main.vcenter.control.instances import Instance

from app.main.base import control as base_control
from app.main.base.apis.auth import basic_auth


parser = reqparse.RequestParser()

parser.add_argument('platform_id')  # 平台ID
parser.add_argument('snapshot_id')  # 快照ID
parser.add_argument('vm_uuid')  # 虚拟机uuid
parser.add_argument('snapshot_name')  # 快照名称
parser.add_argument('description')  # 快照说明
parser.add_argument('action')  # 操作
parser.add_argument('pgnum')  # 页码


class SnapshotManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
         获取vm 快照
        ---
       tags:
          - vCenter snapshot
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: query
            name: vm_uuid
            type: string
            description: vm_uuid
          - in: query
            name: snapshot_id
            type: string
            description: snapshot_id
          - in: query
            name: pgnum
            type: integer
            description: 页码
       responses:
          200:
            description: 获取vm snapshot 信息
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
                  default: "操作成功"
                data:
                  type: array
                  items:
                    properties:
                      create_time:
                        type: string
                        default: 2019-04-08 14:09:40
                        description: create_time
                      current:
                        type: string
                        default: true
                        description: current
                      description:
                        type: string
                        default: internal-template-snapshot
                        description: description
                      id:
                        type: string
                        default: 1
                        description: id
                      mor_name:
                        type: string
                        default: snapshot-739
                        description: mor_name
                      name:
                        type: string
                        default: internal-template-snapshot
                        description: name
                      snapshot_id:
                        type: string
                        default: 1
                        description: snapshot_id
                      snapshot_parent_id:
                        type: string
                        default: null
                        description: snapshot_parent_id
                      state:
                        type: string
                        default: poweredOff
                        description: state
                      vm_uuid:
                        type: string
                        default: 420181c1-ff55-fde5-1b16-1568bd38c6b3
                        description: vm_uuid
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
        try:
            pgnum = args['pgnum'] if args['pgnum'] else 1
            data, pg = control.snapshots.get_snapshot_list(platform_id=args['platform_id'],
                                                           snapshot_id=args['snapshot_id'],
                                                           vm_uuid=args['vm_uuid'], pgnum=pgnum)
        except Exception as e:
            return set_return_val(False, [], str(e), 6101), 400
        return set_return_val(True, data, 'Snapshot gets success.', 6100, pg)

    @basic_auth.login_required
    def post(self):
        """
         根据vm  创建快照信息
        ---
       tags:
          - vCenter snapshot
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
              - vm_uuid
              - snapshot_name
              - action
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                vm_uuid:
                  type: string
                  default: 42018ddf-f886-12b5-a652-dd60b04ca2df
                  description: 云主机uuid
                  example: 42018ddf-f886-12b5-a652-dd60b04ca2df
                snapshot_name:
                  type: string
                  default: 1
                  description: 快照名称
                  example: 快照_vm1
                description:
                  type: string
                  default: 1
                  description: 描述
                  example: 快照_20190501
                action:
                  type: string
                  default: 1
                  description: 操作 create revert
                  example: create
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
                  default: "操作成功"
                data:
                  type: array
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
            type='vm_snapshot',
            result=False,
            resources_id=None,
            event=unicode('生成/恢复快照'),
            submitter=g.username,
        )
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            if args['action'] == 'create':
                if not args['snapshot_name']:
                    g.error_code = 6152
                    raise Exception('Parameter error')
                instance.add_snapshot(snapshot_name=args['snapshot_name'], description=args['description'])
                g.error_code = 6150
                data['event'] = unicode('生成快照')
                data['result'] = True
            elif args['action'] == 'revert':
                if not args['snapshot_id']:
                    g.error_code = 6152
                    raise Exception('Parameter error')

                instance.snapshot_revert(snapshot_id=args['snapshot_id'])
                g.error_code = 6153
                data['event'] = unicode('恢复快照')
                data['result'] = True
            else:
                g.error_code = 2305
                raise Exception('Parameter error')
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = args.get('vm_uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'snapshot update success.', g.error_code)

    @basic_auth.login_required
    def delete(self):
        """
         根据 vm  删除快照信息
        ---
       tags:
          - vCenter snapshot
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: string
            description: platform_id
            required: true
          - in: query
            name: vm_uuid
            type: string
            description: vm_uuid
            required: true
          - in: query
            name: snapshot_id
            type: string
            description: snapshot_id
            required: true
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
                  default: "操作成功"
                data:
                  type: array
                  items:
                    properties:
          400:
            description: 删除失败
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
                  default: "删除失败"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        data = dict(
            type='vm_snapshot',
            result=False,
            resources_id=None,
            event=unicode('删除快照'),
            submitter=g.username,
        )
        try:
            instance = Instance(platform_id=args['platform_id'], uuid=args['vm_uuid'])
            instance.delete_snapshot(snapshot_id=args['snapshot_id'])
            data['result'] = True
        except Exception as e:
            return set_return_val(False, [], str(e), 6201), 400
        finally:
            data['resources_id'] = args.get('vm_uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'snapshot delete success.', 6200)
