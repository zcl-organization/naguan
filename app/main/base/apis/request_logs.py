# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.control.request_logs import log_list_c, log_delete_c

parser = reqparse.RequestParser()
parser.add_argument('request_id', type=str)
parser.add_argument('status_num', type=int)
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
            name: page
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
        request_id = args.get('request_id')
        status_num = args.get('status_num')
        page = args.get('pgnum')
        if not page:
            page = 1  # 默认第一页
        options = {
            'page': page,
            'request_id': request_id,
            'status_num': status_num,
        }
        if log_list_c(options=options):
            request_logs, pg = log_list_c(options=options)
            response_data['code'] = 1200
            response_data['ok'] = True
            response_data['data'] = request_logs
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
        response_data['data'] = ''
        response_data['pg'] = ''
        if id:
            result = log_delete_c(id=id)
            if result:
                response_data['msg'] = '删除成功'
                response_data['ok'] = True
                response_data['code'] = 1200
            else:
                response_data['msg'] = '不存在的请求日志ID'
                response_data['code'] = 3005
                response_data['ok'] = False
            return response_data
        else:
            response_data['msg'] = '请输入ID'
            response_data['code'] = 3005
            response_data['ok'] = False
            return response_data

