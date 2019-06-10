# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('platform_id')


class InstanceTemplateManage(Resource):
    def get(self):

        pass

    def delete(self, vm_uuid):
        pass
