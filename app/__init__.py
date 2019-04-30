# -*- coding:utf-8 -*-
from flask import Flask, jsonify

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

# from celery import Celery
#
# celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL)


# def make_celery(app):
#     celery = Celery(app.import_name)
#     celery.conf.update(app.config)
#     return celery


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    app.config.from_object(config[config_name])
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    config[config_name].init_app(app)

    # datastore = SQLAlchemyUserDatastore(db, Users, Roles)
    # Security(app, datastore)

    # system_config = SystemConfig.query.first()
    # SystemConfig.query.first()
    # if system_config:
    #     print(system_config.copyright)
    Session(app)
    init_ext(app)
    restful_init(app)
    swagger_init(app)
    security_init(app)

    celery.conf.update(app.config)
    # celery.init_app(app=app)

    # from app.main.auth import auth
    # app.register_blueprint(auth)
    # from main import main_v1_bp
    # app.register_blueprint(main_v1_bp)

    # app.register_blueprint(auth, url_prefix='/api_v1')

    @app.route('/')
    def index():
        # print('is_active:', current_user.is_active)
        data = {
            'status': 1,
            'msg': 'success',
            'data': 'hhhhh'
        }
        return jsonify(data)

    return app
