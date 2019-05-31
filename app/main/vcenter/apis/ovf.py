# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from app.main.vcenter import control

parser = reqparse.RequestParser()

parser.add_argument('ovf_id')  # 模板id


class OvfManage(Resource):
    def get(self):
        control.ovf.ovf_list()
