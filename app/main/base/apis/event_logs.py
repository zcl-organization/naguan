# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base.control.event_logs import log_list, log_delete
from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('event_request_id', type=str)
parser.add_argument('task_request_id', type=str)
parser.add_argument('operation_resources_id', type=str)
parser.add_argument('submitter', type=str)
parser.add_argument('pgnum', type=int)
response_data = {}


class LogEvent(Resource):

    def get(self):
        """
        获取事件日志信息
        ---
        tags:
          - logs
        summary: 事件日志
        parameters:
          - in: query
            name: event_request_id
            type: string
            description: 请求id
          - in: query
            name: task_request_id
            type: string
            description: 任务id
          - in: query
            name: pgnum
            type: int
            description: 页码
          - name: submitter
            type: string
            in: query
            description: 提交者
          - name: operation_resources_id
            type: string
            in: query
            description: 资源id
        responses:
          200:
            description: 事件日志信息
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
                        default: 1
                      event_request_id:
                        type: string
                        default: 4418f216-5956-5df7-a33c-990c2f53e5c8
                      operation_event:
                        type: string
                        default: 4418f216-5956-5df7-a33c-990c2f53e5c8
                      operation_resources_id:
                        type: string
                        default: 1111
                      resource_type:
                        type: string
                        default: menu
                      result:
                        type: string
                        default: 1
                      submitter:
                        type: string
                        default: anonymous
                      task_request_id:
                        type: string
                        default: 4418f216-5956-5df7-a33c-990c2f53e5c8
                      time:
                        type: string
                        default: 2019-05-20 10:17:40

        """
        args = parser.parse_args()
        pgnum = args['pgnum']
        # event_request_id = args.get('event_request_id')
        # task_request_id = args.get('task_request_id')
        # submitter = args.get('submitter')
        # operation_resources_id = args.get('operation_resources_id')
        if not pgnum:
            pgnum = 1  # 默认第一页

        try:

            data, pg = control.event_logs.log_list(pgnum=pgnum, event_request_id=args['event_request_id'],
                                                   task_request_id=args['task_request_id'], submitter=args['submitter'],
                                                   operation_resources_id=args['operation_resources_id'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1821), 400
        return set_return_val(True, data, 'request log list succeeded.', 1820, pg)

    def delete(self, id):
        """
        根据事件日志id删除信息
       ---
       tags:
          - logs
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
           description: 根据事件日志id删除信息
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
            g.error_code = 1841
            result = control.event_logs.log_delete(log_id=id)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        return set_return_val(True, [], 'request log deleted succeeded.', 1840)
