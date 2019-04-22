# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.control.task_logs import log_list_c, log_delete_c

parser = reqparse.RequestParser()
parser.add_argument('task_id', type=str)
parser.add_argument('rely_task_id', type=str)
parser.add_argument('request_id', type=str)
parser.add_argument('submitter', type=str)
parser.add_argument('pgnum', type=int)
response_data = {}


class LogTask(Resource):

    def get(self):
        """
        获取任务日志信息
        ---
        tags:
          - logs
        summary: Add a new pet to the store
        parameters:
          - in: query
            name: task_id
            type: string
            description: 任务id
          - in: query
            name: rely_task_id
            type: string
            description: 依赖任务id
          - in: query
            name: page
            type: int
            description: 页码
          - name: submitter
            type: string
            in: query
            description: 提交者
          - name: request_id
            type: string
            in: query
            description: 请求id
        responses:
          200:
            description: A single logs item a
            schema:
              id: EventLog
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        args = parser.parse_args()
        task_id = args.get('task_id')
        rely_task_id = args.get('rely_task_id')
        request_id = args.get('request_id')
        submitter = args.get('submitter')
        page = args.get('pgnum')
        if not page:
            page = 1  # 默认第一页
        options = {
            'page': page,
            'task_id': task_id,
            'rely_task_id': rely_task_id,
            'request_id': request_id,
            'submitter': submitter,
        }
        if log_list_c(options=options):
            task_logs, pg = log_list_c(options=options)
            response_data['code'] = 1200
            response_data['ok'] = True
            response_data['data'] = task_logs
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

    def delete(self, id=None):
        """
        根据任务日志id删除信息
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
           description: 根据任务日志id删除信息
           schema:
             id: TaskLog
             properties:
               username:
                 type: string
                 description: The name of the task_logs
                 default: Steven Wilson
        """
        response_data['data'] = ''
        response_data['pg'] = ''
        if id:
            result = log_delete_c(id=id)
            if result:
                response_data['msg'] = '删除成功'
            else:
                response_data['msg'] = '不存在的任务日志ID'
                response_data['code'] = 3005
                response_data['status'] = 'failed'
                response_data['ok'] = False
            return response_data
        else:
            response_data['msg'] = '请输入ID'
            response_data['code'] = 3005
            response_data['status'] = 'failed'
            response_data['ok'] = False
            return response_data



