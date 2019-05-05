# -*- coding:utf-8 -*-
import os
import werkzeug
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.models import SystemConfig
import sys
from app.exts import db
from config import UPLOAD_DIR
from app.main.base import control

reload(sys)
sys.setdefaultencoding('utf8')
parser = reqparse.RequestParser()
parser.add_argument('logo', type=werkzeug.datastructures.FileStorage, location='files', required=True, help='请上传logo')


class SystemLogo(Resource):
    def put(self):
        """
            update logo
            ---
            tags:
             - system config
            parameters:
            - name: "logo"
              in: "formData"
              required: true
              type: file
              format: "int64"
            responses:
                200:
                  description: "successful operation"
        """
        args = parser.parse_args()
        try:
            logo = args['logo']
            control.system.system_config_update_logo(logo)
        except Exception as e:
            return set_return_val(False, [], str(e), 1319), 400
        return set_return_val(True, [], 'System logo upload succeeded', 1300)
        # system = SystemConfig.query.get(1)
        # if system:
        #     args = parser.parse_args()
        #     # 读取logo文件
        #     logo_file = args.get('logo')
        #     # logo名称
        #     logo_name = logo_file.filename
        #     # logo保存路径
        #     logo_path = os.path.join(UPLOAD_DIR, logo_name)
        #     # 保存
        #
        #     # print UPLOAD_DIR
        #     logo_file.save(logo_path)
        #     # 更新数据库
        #     system.logo = UPLOAD_DIR + logo_name
        #     # print system.logo
        #     db.session.add(system)
        #     db.session.commit()
        #     response_data = {
        #         'ok': True,
        #         'code': 200,
        #         'msg': 'logo更新成功',
        #         'logo': system.logo,
        #     }
        #     return response_data
        # else:
        #     response_data = {
        #         'code': 401,
        #         'msg': '系统配置不存在,logo上传失败',
        #         'ok': False,
        #         'data': '',
        #     }
        #     return response_data
