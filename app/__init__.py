# -*- coding:utf-8 -*-
from flask import Flask, jsonify

from app.common.tool import set_return_val
from app.models import Roles, Users, SystemConfig
from flask_security import Security, SQLAlchemyUserDatastore

from app.main.base.apis.auth import basic_auth
from app.exts import db
from config import config, BaseConfig
from app.exts import init_ext
from app.main import restful_init
from app.main import swagger_init
from app.main.base.control.roles_users import security_init
from flask_session import Session

from app.exts import celery


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    app.config.from_object(config[config_name])
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    config[config_name].init_app(app)

    Session(app)
    init_ext(app)
    restful_init(app)
    swagger_init(app)
    security_init(app)

    celery.conf.update(app.config)

    @app.route('/')
    def index():
        # print('is_active:', current_user.is_active)
        data = {
            'status': 1,
            'msg': 'success',
            'data': 'hhhhh'
        }
        return jsonify(data)

    @app.route('/api/v1.0/unauthorized')
    def unauthorized():
        data = {
            'ok': False,
            'data': [],
            'msg': 'operation is not authorized',
            'code': 1000

        }
        return jsonify(data), 400

    return app
