# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import g
from app import set_return_val
from app.main.base import control
from auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('company_name')
parser.add_argument('company_mobile')
parser.add_argument('company_fax')
parser.add_argument('company_remarks')
parser.add_argument('company_id')
parser.add_argument('principal_id')
parser.add_argument('principal_name')


class CompanyManage(Resource):
    @basic_auth.login_required
    def get(self):
        """
        获取单位信息
        ---
       tags:
           - company
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: company_id
            type: string
          - in: query
            name: company_name
            type: string
          - in: query
            name: principal_name
            type: string
       responses:
          200:
            description: 获取单位信息
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
                      company_name:
                        type: string
                        default: company_name
                        description: 单位名称
                        example: 什么马科技
                      company_mobile:
                        type: string
                        default: company_mobile
                        description: 单位电话
                        example: 13114545454
                      company_id:
                        type: string
                        default: 1
                        description: 单位编号
                        example: 1
                      company_fax:
                        type: string
                        default: company_fax
                        description: 单位传真
                        example: 0591-87111111
                      company_remarks:
                        type: string
                        default: company_remarks
                        description: 单位备注
                        example: 什么码科技有限公司
                      principal_id:
                        type: string
                        default: 1
                        description: 负责人编号
                        example: 1
                      principal_name:
                        type: string
                        default: 张三丰
                        description: 负责人名称
                        example: 张三丰
        """
        args = parser.parse_args()

        try:
            company = control.company.get_company(company_id=args['company_id'], name=args['company_name'],
                                                  principal_name=args['principal_name'])

        except Exception as e:
            company = None
            print('failed')
        return set_return_val(True, company, 'get company successfully', 1200)

    @basic_auth.login_required
    def post(self):
        """
        提交单位信息
        ---
       tags:
           - company
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
              - company_name
              - company_mobile
              properties:
                company_name:
                  type: string
                  default: 什么马科技
                  description: 单位名称
                  example: 什么马科技
                company_mobile:
                  type: string
                  default: 13114545454
                  description: 单位联系号码
                  example: 13114545454
                company_fax:
                  type: string
                  default: index
                  description: 单位传真号码
                  example: 0591-87111111
                company_remarks:
                  type: string
                  default: 1
                  description: 单位备注
                  example: 什么马科技有限股份公司
                principal_id:
                  type: integer
                  default: 1
                  description: 负责人编号
                  example: 1
       responses:
          200:
            description: 提交单位信息
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
                      company_id:
                        type: string
                        default: 1
                        description: 单位编号
                        example: 1
                      company_name:
                        type: string
                        default: 什么马科技
                        description: 单位名称
                        example: 什么马科技
                      company_mobile:
                        type: string
                        default: 13114545454
                        description: 单位联系号码
                        example: 13114545454
                      company_fax:
                        type: string
                        default: 0591-87111111
                        description: 单位传真号码
                        example: 0591-87111111
                      company_remarks:
                        type: string
                        default: 什么马科技有限公司
                        description: 备注
                        example: 什么马科技有限公司
                      principal_id:
                        type: string
                        default: 1
                        description: 负责人编号
                        example: 1
        """
        args = parser.parse_args()
        data = dict(
            type='company',
            result=True,
            resources_id=None,
            event=unicode('添加单位信息'),
            submitter=g.username,
        )
        try:
            if not all([args['company_name'], args['company_mobile']]):
                raise Exception('Parameter error')

            company = control.company.create_company(company_name=args['company_name'],
                                                     company_mobile=args['company_mobile'],
                                                     company_fax=args['company_fax'], principal_id=args['principal_id'],
                                                     company_remarks=args['company_remarks'])

            data['resources_id'] = company['company_id']
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 404), 400
        finally:
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, company, 'Create company successfully', 1200)

    @basic_auth.login_required
    def put(self, company_id):
        """
        更新单位信息
        ---
       tags:
           - company
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: company_id
           type: integer
           format: int64
           required: true
         - in: formData
           name: company_name
           type: string
         - name: company_mobile
           type: string
           in: formData
         - name: company_fax
           type: string
           in: formData
         - name: company_remarks
           type: string
           in: formData
         - name: principal_id
           type: integer
           format: int64
           in: formData
       responses:
         200:
            description: 更新单位信息
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
        data = dict(
            type='company',
            result=False,
            resources_id=None,
            event=unicode('更新单位信息'),
            submitter=g.username
        )
        try:
            args = parser.parse_args()
            if not company_id:
                raise Exception('Parameter error')
            control.company.update_company_by_id(company_id=company_id, company_name=args['company_name'],
                                                 company_mobile=args['company_mobile'], company_fax=args['company_fax'],
                                                 principal_id=args['principal_id'],
                                                 company_remarks=args['company_remarks'])
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = company_id
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'company update success.', 2020)

    @basic_auth.login_required
    def delete(self, company_id):
        """
        删除单位信息
        ---
       tags:
          - company
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
         - in: path
           name: company_id
           type: integer
           format: int64
           required: true
       responses:
         200:
            description: 删除用户信息
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
        data = dict(
            type='company',
            result=False,
            resources_id=None,
            event=unicode('删除单位信息'),
            submitter=g.username
        )
        try:
            if not company_id:
                raise Exception('Parameter error')
            control.company.delete_company_by_id(company_id)
        except Exception as e:
            return set_return_val(False, [], str(e), g.error_code), 400
        finally:
            data['resources_id'] = company_id
            control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'company delete success.', 2020)
