# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()
parser.add_argument('platform_id')  # 平台ID


class LicenseManage(Resource):

    @basic_auth.login_required
    def get(self):
        try:
            args = parser.parse_args()
            data = control.license.find_license(platform_id=args['platform_id'])
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001), 400
        return set_return_val(True, data, 'License info get Success!', 3000)

    def post(self):
        args = parser.parse_args()
        control.license.create_licenses(platform_id=args['platform_id'])
        return set_return_val(True, [], 'License info create Success!', 3000)
