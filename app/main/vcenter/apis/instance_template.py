# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app import set_return_val
from app.main.vcenter.control.instances import Instance

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('pgnum')
parser.add_argument('pgsort')
parser.add_argument('host')
parser.add_argument('vm_name')


class InstanceTemplateManage(Resource):

    def get(self):
        args = parser.parse_args()
        try:
            instance = Instance(platform_id=args['platform_id'])

            pgnum = args['pgnum'] if args['pgnum'] else 1

            data, pg = instance.list(host=args['host'], vm_name=args['vm_name'], pgnum=pgnum,
                                     pgsort=args['pgsort'], template=True)
        except Exception as e:
            return set_return_val(False, [], str(e), 2031), 400
        return set_return_val(True, data, 'instance gets success.', 2030, pg), 200

    def post(self):
        args = parser.parse_args()

        instance = Instance(platform_id=args['platform_id'])

        pass

    def delete(self, vm_uuid):
        pass
