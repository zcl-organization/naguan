# -*- coding:utf-8 -*-
from app.main.base.db import user as db_user
from app.common.my_exceptions import ExistsException
from app.main.base import db


# 获取用户列表
def user_list(user_id, email, mobile, remarks, next_page, limit):
    try:
        result, pg = db_user.user_list(user_id, email, mobile, remarks, next_page, limit)
        userinfo = []
        for user in result:
            user = {
                'name': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'uid': user.uid,
                'id': user.id,
                'mobile': user.mobile,
                'department': user.department,
                'job': user.job,
                'location': user.location,
                'company': user.company,
                'sex': user.sex,
                'uac': user.uac,
                'date_created': user.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'last_login_at': user.last_login_at.strftime('%Y-%m-%d %H:%M:%S'),
                'last_login_ip': user.last_login_ip,
                'current_login_ip': user.current_login_ip,
                'login_count': user.login_count
            }
            userinfo.append(user)
    except Exception as e:
        raise Exception('User information get failed')
    return userinfo, pg


# 创建用户信息
def user_create(username, password, email, first_name, uid, mobile, department, job, location, company, sex, uac,
                active, is_superuser, remarks, current_login_ip):
    # 判断是否已存在用户名相同的用户
    # print(email)
    user = db.user.user_list_by_name(username)

    if not user:
        # 判断是否已存在用户名相同的用户
        user_email = db.user.user_list_by_email(email)
        if not user_email:
            return db.user.user_create(username, password, email, first_name, uid, mobile, department, job, location,
                                       company, sex, uac, active, is_superuser, remarks, current_login_ip)
        else:
            raise ExistsException('user', email)
    else:
        raise ExistsException('user', username)


# 删除用户信息
def user_delete(id=None):
    # 判断是否有用户
    user = db.user.user_list_by_id(id)
    if user:
        return db.user.user_delete(id)
    else:
        raise Exception('no user')


# 更新用户信息
def user_update(id, active, username, password, mobile, company, department, remarks):
    # 判断是否有用户
    # print('update user')
    user = db.user.user_list_by_id(id)
    if user:
        # print('has user')
        # 更新用户信息
        return db.user.user_update(id, active, username, password, mobile, company, department, remarks)
    else:
        raise Exception('no user')


def user_list_by_id(id):
    user = db.user.user_list_by_id(id)
    return user


def list_by_name(username):
    return db.user.user_list_by_name(username)


def update_login_time(user):
    return db.user.update_login_time(user)
