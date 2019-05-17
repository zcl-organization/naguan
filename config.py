# -*- coding:utf-8 -*-
import os
from os import getenv
import redis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'app\\static\\img\\')


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_SALT = 'xxxxxxxxxxxxxxxxxxxxx'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECRET_KEY = 'cccxdfcccc'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='118.24.10.85', port='6379', password='123456')
    SESSION_KEY_PREFIX = 'flask'
    # CELERY_IMPORTS = ('tasks.add',)
    CELERY_BROKER_URL = 'redis://:123456@118.24.10.85:6379/'
    CELERY_RESULT_BACKEND = 'redis://:123456@118.24.10.85:6379/'

    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    SQLALCHEMY_RECORD_QUERIES = True

    LOG_PATH = os.path.join(BASE_DIR, 'app\\static\\logs')
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    # 轮转数量是 10 个
    LOG_FILE_BACKUP_COUNT = 10
    # LDAP = {
    #     'URI': 'ldap://10.5.17.25/',
    #     'BIND_DN': 'cn=%(username)s,ou=17173_users,dc=17173-family,dc=com',  # Bind directly to this base DN.
    #     'KEY_MAP': {  # Map ldap keys into application specific keys
    #         'username': 'cn',
    #         'first_name': 'displayName',
    #         'email': 'mail',
    #         'mobile': 'telephoneNumber',
    #         'department': 'description',
    #         'job': 'title',
    #         'location': 'physicalDeliveryOfficeName',
    #         'company': 'company',
    #         'sex': 'info',
    #         'uac': 'userAccountControl',
    #     },
    #     'OPTIONS': {  # LDAP connection options
    #         'OPT_PROTOCOL_VERSION': 3,
    #     },
    # }
    LDAP = {
        'LDAP_HOST': 'ldap://192.168.12.30/',
        'LDAP_BASE_DN': 'dc=mypass,dc=com',
        'LDAP_USER_DN': 'ou=users',
        'LDAP_GROUP_DN': 'ou=groups',
        'LDAP_USER_RDN_ATTR': 'cn',
        'LDAP_USER_LOGIN_ATTR': 'mail',
        'LDAP_BIND_USER_DN': None,
        'LDAP_BIND_USER_PASSWORD': None
    }
    SSO = {
        # "app_name": getenv("sso_app_name", "naguan_base_demo"),
        "app_name": getenv("sso_app_name", "dbaas_kstack_demo"),

        # SSO中注册的应用名

        "app_id": getenv("sso_app_id", "2934880e56ad75758ee8e8151d1e4ded"),
        # SSO中注册返回的`app_id`

        "app_secret": getenv("sso_app_secret", "GIZTOMBTMRRGCMRVMIZDINZUMU4GMY3EGY3G"),
        # SSO中注册返回的`app_secret`

        "sso_server": getenv("sso_server", "http://sso.kaopuvm.com/"),
        # SSO完全合格域名根地址
        "HMAC_SHA256_KEY": getenv("hmac_sha256_key", "37af01c8d797fa715827c7408ae67a1b"),
        # hmac sha256 key (与passport一致)

        "AES_CBC_KEY": getenv("aes_cbc_key", "R3Qx5RHbqrVG49Ox"),
        # auth.aes_cbc.CBC类中所用加密key (与passport一致, 限制16位)

        "JWT_SECRET_KEY": getenv("jwt_secret_key",
                                 "kP37@.2BC3B90x.5T1v31c-V73F93C+DZYn0+xzwM+YzVb12nZ25=3O3MKJdl.24Yx,137V")
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'develop.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aaaaaa@192.168.125.160:3306/Code3?charset=utf8'


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aaaaaa@192.168.125.160:3306/Code3?charset=utf8'


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aaaaaa@192.168.125.160:3306/Code3?charset=utf8'


config = {
    'develop': DevelopConfig,  # 开发环境
    'testing': TestingConfig,  # 测试环境
    'product': ProductConfig,  # 线上环境
    'default': DevelopConfig,  # 默认环境
}
