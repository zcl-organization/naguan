# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.control.event_logs import log_list_c, log_delete_c

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
        summary: Add a new pet to the store
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
            name: page
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
            description: A single logs item
            schema:
              id: EventLog
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        args = parser.parse_args()
        page = args.get('pgnum')
        event_request_id = args.get('event_request_id')
        task_request_id = args.get('task_request_id')
        submitter = args.get('submitter')
        operation_resources_id = args.get('operation_resources_id')
        if not page:
            page = 1  # 默认第一页
        options = {
            'page': page,
            'event_request_id': event_request_id,
            'submitter': submitter,
            'task_request_id': task_request_id,
            'operation_resources_id': operation_resources_id,
        }
        if log_list_c(options=options):
            event_logs, pg = log_list_c(options=options)
            response_data['code'] = 1200
            response_data['ok'] = True
            response_data['data'] = event_logs
            response_data['msg'] = '获取日志信息成功'
            response_data['pg'] = pg
            return response_data
        else:
            response_data['code'] = 1204
            response_data['msg'] = '搜索日志结果不存在'
            response_data['ok'] = False
            response_data['data'] = ''
            response_data['pg'] = ''
            return response_data

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
             id: EventLog
             properties:
               username:
                 type: string
                 description: The name of the event_logs
                 default: Steven Wilson
        """
        response_data['data'] = ''
        response_data['pg'] = ''
        if id:
            result = log_delete_c(id=id)
            if result:
                response_data['msg'] = '删除成功'
                response_data['ok'] = True
                response_data['code'] = 1200
            else:
                response_data['msg'] = '不存在的事件日志ID'
                response_data['code'] = 3005
                response_data['ok'] = False
            return response_data
        else:
            response_data['msg'] = '请输入ID'
            response_data['code'] = 3005
            response_data['ok'] = False
            return response_data




