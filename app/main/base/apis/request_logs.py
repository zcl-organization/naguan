# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val

from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('request_id', type=str)
parser.add_argument('submitter', type=str)
parser.add_argument('status', type=int)
parser.add_argument('pgnum', type=int)
parser.add_argument('time_start', type=int)
parser.add_argument('end_at', type=int)
response_data = {}


class LogRequest(Resource):

    def get(self):
        """
        获取请求日志信息
        ---
        tags:
          - logs
        summary: 请求日志信息
        parameters:
          - in: query
            name: request_id
            type: string
            description: 请求id
          - in: query
            name: submitter
            type: string
            description: 提交者
          - in: query
            name: pgnum
            type: int
            description: 页码
          - name: status
            type: int
            in: query
            description: 状态码
        responses:
          200:
            description: 请求日志信息
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
                      ip:
                        type: string
                        default: 127.0.0.1
                      request_id:
                        type: string
                        default: bd14307d-1dc0-57c5-bde8-0e44fa4a9903
                      status:
                        type: string
                        default: 200
                      submitter:
                        type: string
                        default: anonymous
                      time:
                        type: string
                        default: 2019-05-17 16:05:37
                      url:
                        type: string
                        default: GET/http://127.0.0.1:5000/api/v1.0/vCenter/tree
        """
        args = parser.parse_args()
        pgnum = args['pgnum']

        if not pgnum:
            pgnum = 1  # 默认第一页
        try:
            data, pg = control.request_logs.log_list(pgnum=pgnum, request_id=args['request_id'],
                                                     status_num=args['status'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1731), 400
        return set_return_val(True, data, 'request log list succeeded.', 1730, pg)

    def delete(self, id):
        """
        根据请求日志id删除信息
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
           description: 根据请求日志id删除信息
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
            result = control.request_logs.log_delete(id=id)
        except Exception as e:
            return set_return_val(False, [], str(e), 1711), 400
        return set_return_val(True, [], 'request log deleted succeeded.', 1710)
