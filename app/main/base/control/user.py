# -*- coding:utf-8 -*-
from app.main.base.db import user as db_user
from app.common.my_exceptions import ExistsException


# 获取用户列表
def user_list(options=None):
    return db_user.user_list(options)


# 创建用户信息
def user_create(options=None):
    # 判断是否已存在用户名相同的用户
    user = db_user.user_list_by_name(options['username'])

    if not user:
        # 判断是否已存在用户名相同的用户
        email = db_user.user_list_by_email(options['email'])
        if not email:
            return db_user.user_create(options)
        else:
            raise ExistsException('user', options['email'])
    else:
        raise ExistsException('user', options['username'])


# 删除用户信息
def user_delete(id=None):
    # 判断是否有用户
    user = db_user.user_list_by_id(id)
    if user:
        return db_user.user_delete(id)
    else:
        return False


# 更新用户信息
def user_update(id, options=None):
    # 判断是否有用户
    # print('update user')
    user = db_user.user_list_by_id(id)
    if user:
        # print('has user')
        # 更新用户信息
        return db_user.user_update(id, options)
    else:
        return False


def user_list_by_id(id):
    user = db_user.user_list_by_id(id)
    return user
