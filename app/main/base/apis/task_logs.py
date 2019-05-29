# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base import control

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
            name: pgnum
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
            description: 任务日志信息
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
                        type: int
                        default: 1
                      await_execute:
                        type: string
                        default: 1/2
                      end_time:
                        type: string
                        default: 2019-05-20 15:59:26.096000
                      enqueue_time:
                        type: string
                        default: 2019-05-20 15:58:26.096000
                      method_name:
                        type: string
                        default: sync_tree
                      queue_name:
                        type: string
                        default: vsphere
                      rely_task_id:
                        type: string
                        default: --
                      request_id:
                        type: string
                        default: 96be5461-abb2-508f-aba5-38cf027efe48
                      start_time:
                        type: string
                        default: None
                      status:
                        type: string
                        default: wait
                      submitter:
                        type: string
                        default: anonymous
                      task_id:
                        type: string
                        default: eb054bcd-3360-4eff-a10d-1f2c35a977fb

        """
        args = parser.parse_args()
        task_id = args.get('task_id')
        rely_task_id = args.get('rely_task_id')
        request_id = args.get('request_id')
        submitter = args.get('submitter')
        pgnum = args.get('pgnum')
        if not pgnum:
            pgnum = 1  # 默认第一页
        options = {
            'page': pgnum,
            'task_id': task_id,
            'rely_task_id': rely_task_id,
            'request_id': request_id,
            'submitter': submitter,
        }

        try:

            data, pg = control.task_logs.log_list(pgnum=pgnum, task_id=args['task_id'],
                                                  rely_task_id=args['rely_task_id'], submitter=args['submitter'],
                                                  request_id=args['request_id'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1931), 400
        return set_return_val(True, data, 'request log list succeeded.', 1930, pg)

    def delete(self, id):
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
            control.task_logs.log_delete(id)
        except Exception as e:
            return set_return_val(False, [], str(e), 1911), 400
        return set_return_val(True, [], 'request log deleted succeeded.', 1910)
