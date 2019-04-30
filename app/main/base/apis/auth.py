# -*- coding:utf-8 -*-
from flask import jsonify, current_app, request, url_for, redirect, g, make_response,session

from flask_security import login_required, login_user, roles_accepted
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask_restful import Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from app.models import Users
from config import config
from flask_ldap3_login import LDAP3LoginManager
from app.common.aes_cbc import CBC
from app.common.jwtutil import JWTUtil

import requests
import os

current_config = os.getenv('FLASK_CONFIG') or 'default'
config_dict = config[current_config]


# config_dict.SSO
sso_server = config_dict.SSO
cbc = CBC()
jwtutil = JWTUtil()


# sso_server = SSO.get("sso_server").strip("/")
# assert url_check(sso_server) is True

def unauthorized():
    return jsonify({
        'error': {
            'title': 'InvalidAuthorized',
            'msg': 'Could not verify your access'
        },
        'ok': False
    })


def set_ssoparam(returnurl="/"):
    """生成sso请求参数，5min过期"""
    app_name = sso_server['app_name']
    app_id = sso_server['app_id']
    app_secret = sso_server['app_secret']
    return cbc.encrypt(jwtutil.createJWT(
        payload=dict(app_name=app_name, app_id=app_id, app_secret=app_secret, ReturnUrl=returnurl), expiredSeconds=300))


def sso_request(url, params=None, data=None, timeout=5, num_retries=3):
    """
    @params dict: 请求查询参数
    @data dict: 提交表单数据
    @timeout int: 超时时间，单位秒
    @num_retries int: 超时重试次数
    """
    headers = {"User-Agent": "Mozilla/5.0 (X11; CentOS; Linux i686; rv:7.0.1406) Gecko/20100101 PassportClient/0.1"}
    try:
        resp = requests.post(url, params=params, headers=headers, timeout=timeout, data=data).json()
    except requests.exceptions.Timeout as e:
        # logger.error(e, exc_info=True)
        if num_retries > 0:
            return sso_request(url, params=params, data=data, timeout=timeout, num_retries=num_retries - 1)
    else:
        return resp


class MyHTTPBasicAuth(HTTPBasicAuth):
    """ 访问方式
        from requests.auth import HTTPBasicAuth
        requests.get(url, auth=HTTPBasicAuth(user, pswd))
    """

    def authenticate_header(self):
        # 解决401时弹窗问题
        return 'x{}'.format(super(MyHTTPBasicAuth, self).authenticate_header())

    def error_handler(self, f=None):
        f = unauthorized
        return super(MyHTTPBasicAuth, self).error_handler(f)


basic_auth = MyHTTPBasicAuth()

ret_data = {
    'ok': True,
    'data': {}
}



parser = reqparse.RequestParser()
parser.add_argument('Action')
parser.add_argument('ticket')
parser.add_argument('id')
parser.add_argument('ReturnUrl')
parser.add_argument('NextUrl')


class AuthManage(Resource):
    def post(self):

        args = parser.parse_args()

        if args['Action'] == 'ssoLogin':
            ticket = args['ticket']
            if ticket:
                get_userinfo = True
                get_userbind = False
                resp = sso_request("{}/sso/validate".format(sso_server['sso_server']),
                                   dict(Action="validate_ticket"),
                                   dict(ticket=ticket, app_name=sso_server["app_name"],
                                        get_userinfo=get_userinfo,
                                        get_userbind=get_userbind))
                if resp and isinstance(resp, dict) and "success" in resp and "uid" in resp:
                    if resp["success"] is True:
                        uid = resp["uid"]
                        sid = resp["sid"]
                        expire = int(resp["expire"])
                        userinfo = resp.get("userinfo") or {}
                        # logger.debug("User info: {}".format(userinfo))
                        # 授权令牌验证通过，设置局部会话，允许登录
                        # sessionId = gen_sessionId(uid=uid, seconds=expire, sid=sid)

                        redirect_url = args['ReturnUrl'] or args['NextUrl']
                        if not redirect_url:
                            redirect_url = url_for('AuthManage')

                        response = make_response(redirect(redirect_url))
                        # response.set_cookie(key="sessionId", value=sessionId, max_age=expire, httponly=True,
                        #                     secure=False if request.url_root.split("://")[0] == "http" else True)
                        response.set_cookie(key="sessionId", max_age=expire, httponly=True,
                                            secure=False if request.url_root.split("://")[0] == "http" else True)
                        # 更新passport的uid到本地
                        if userinfo.get('identifier'):
                            user = Users.query.filter_by(username=userinfo['identifier']).first()
                            if user is None:
                                # user = Users(uid=uid, username=userinfo['identifier'])
                                # db.session.add(user)
                                # User.create(uid=uid, username=userinfo['identifier'])
                                pass
                            else:
                                user.uid = uid
                                # user.update(uid=uid)
                            # db.session.commit()
                        return response

        elif args['Action'] == "ssoLogout":
            pass
        elif args['Action'] == "ssoConSync":
            pass
        return 'error'

        # users = User.query.filter_by(username=args['username']).first()
        # print('status:', users.verify_password(args['password']))
        # if not users or not users.verify_password(args['password']):
        #
        #     ret_data['ok'] = False
        #     ret_data['msg'] = '账号或密码错误'
        #     ret_data['code'] = '1001'
        #
        # else:
        #     login_user(users, True)
        #     token = create_token(users.id, users.username)
        #     data = {
        #         'token': token
        #     }
        #     ret_data['data'] = data
        #     ret_data['code'] = '1000'
        # return ret_data

    # @basic_auth.login_required
    def get(self):
        """
        test
        ---
        tags:
          - auth
        responses:
          200:
            description: 用户登录
            schema:
              id: User
              properties:
                id:
                  type: string
                  description: 用户id
                  default: Steven Wilson
                  name: code
        """
        # print(sso_server['sso_server'])
        sso_url = sso_server['sso_server'].strip("/")
        SSO_ENABLE = True
        if SSO_ENABLE:
            params = {'account': 'front', 'password': 'zzzzzz'}
            ReturnUrl = request.args.get("ReturnUrl") or url_for("AuthManage", _external=True)
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; CentOS; Linux i686; rv:7.0.1406) Gecko/20100101 PassportClient/1111",
                "Origin": "http://sso.kaopuvm.com",
                "Referer": "http://sso.kaopuvm.com/signIn"
            }
            # resp = requests.post('http://sso.kaopuvm.com/signIn', params=params, headers=headers, timeout=5)
            # resp = requests.post('http://sso.kaopuvm.com/signIn', headers=headers)
            # NextUrl = "{}/sso/?sso={}".format(sso_server, set_ssoparam(ReturnUrl))
            # NextUrl = "{}/sso/?sso=".format(sso_server)
            # print(ReturnUrl)
            NextUrl = "{}/sso/?sso={}".format(sso_url, set_ssoparam(ReturnUrl))

            return redirect(NextUrl)
        return 'cesss'


@basic_auth.verify_password
def verify_password(username_or_token, password):
    # 首先验证token
    # print('verify_password')
    # ldap = current_app.config.get('LDAP')
    ldap_manager = LDAP3LoginManager()
    ldap_manager.init_config(current_app.config.get('LDAP'))

    # response = ldap_manager.authenticate(username_or_token, password)
    # print(response.status)

    ldap = False
    if password == '':

        if session.get('token'):
            print('token:', session.get('token'))
            return True
        else:
            print('unable get session')

        data, token_flag = Users.verify_auth_token(username_or_token)
        # data, token_flag = parse_token(username_or_token)
        if token_flag == 1:  # 认证成功
            print('verify success')
            # print(data)
            # g.username = 'zcl'
            # g.user_id = data.username
            # print(data)
            g.username = data['username']
            print(g.username)

        elif token_flag == 2:  # token 超时
            # pass
            return False

        elif token_flag == 3:  # token 解析失败
            return False
    else:
        user = Users.query.filter_by(username=username_or_token).first()
        # g.user_name = username_or_token
        # print(user)
        # print('g.user')
        if user:
            if not user.verify_password(password):
                # print('passwrd error')
                return False
            else:
                # print('password v')
                g.username = username_or_token
                # return True
        elif ldap:
            ldap_manager = LDAP3LoginManager()
            ldap_manager.init_config(current_app.config.get('LDAP'))

            response = ldap_manager.authenticate(username_or_token, password)
            print(response)

        else:
            return False
        login_user(user)
    # user = User.verify_auth_token(username_or_token)
    # if not user:
    #     # 然后再验证用户名和密码
    #     user = User.query.filter_by(username=username_or_token).first()
    #     if not user or not user.verify_password(password):
    #         return False
    # g.user = user
    return True

# auth = Blueprint('auth', __name__, url_prefix='/auth')
#
#
# @auth.route('/login', endpoint='login', methods=['post', 'get'])
# def login():
#     form = LoginForm()
#     # 校验 是否是从form提交进入
#     if not form.validate_on_submit():
#         return render_template('index.html', form=form)
#     else:
#         email = form.email.data
#         password = form.password.data
#         # 未进行密码校验
#         users = User.query.filter_by(email=email).first()
#         if users:
#
#             print('user_id:', users.id)
#             login_user(users, True)
#             # print('url 重定向 到admin 视图')
#             print(url_for('auth.admin'))
#             # return redirect(url_for('admin'))
#             return 'cccc'
#         else:
#             return redirect('/')
#         return '登录成功'
#
#
# @auth.route('/admin', endpoint='admin')
# @set_unauth_view('user')
# @roles_accepted('admin')
# def admin():
#     # print('管理员界面')
#     # print(current_user.has_role('admin'))
#     return 'admin view'
#
#
# @auth.route('/admin/edit', endpoint='admin_edit')
# @set_unauth_view('user')
# @roles_accepted('admin')
# def admin_edit():
#     # print('管理员界面')
#     # print(current_user.has_role('admin'))
#     return 'admin edit view'
#
#
# @auth.route('/admin/<int:id>/test', endpoint='admin_user_test')
# # @set_unauth_view('user')
# @roles_accepted('admin')
# def admin_test(id):
#     # print('管理员界面')
#     # print(current_user.has_role('admin'))
#     return 'admin test  view'
#
#
# @auth.route('/user', endpoint='user')
# @login_required
# def user():
#     return 'user view'
#
#
# @auth.route('/edit', endpoint='edit')
# # @set_unauth_view('/')
# @roles_accepted('admin', 'special-edit')
# def edit():
#     return 'user view'
