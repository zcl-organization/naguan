# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val

from app.main.base import control

parser = reqparse.RequestParser()
parser.add_argument('request_id', type=str)
parser.add_argument('status', type=int)
parser.add_argument('pgnum', type=int)
response_data = {}


class LogRequest(Resource):

    def get(self):
        """
        获取请求日志信息
        ---
        tags:
          - logs
        summary: Add a new pet to the store
        parameters:
          - in: query
            name: request_id
            type: string
            description: 请求id
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
            description: A single logs item
            schema:
              id: RequestLog
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        args = parser.parse_args()
        pgnum = args['pgnum']

        if not pgnum:
            pgnum = 1  # 默认第一页
        try:
            data, pg = control.request_logs.log_list(pgnum=pgnum, request_id=args['request_id'],
                                                     status_num=args['status'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'request log list succeeded.', 1520, pg)

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
             id: RequestLog
             properties:
               username:
                 type: string
                 description: The name of the request_logs
                 default: Steven Wilson
        """

        try:
            result = control.request_logs.log_delete(id=id)
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, [], 'request log deleted succeeded.', 1520)
