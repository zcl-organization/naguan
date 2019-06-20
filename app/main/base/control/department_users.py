# -*- coding:utf-8 -*-

from app.main.base import db
from flask import g
import json


def get_department_users(department_id, user_id):
    department_users = db.department_users.get_department_users(department_id, user_id)
    department_user_list = []
    for item in department_users:
        _t = {
            'department_user_id': item.department_user_id,
            'department_id': item.department_id,
            'user_id': item.user_id,
            'user_name': item.user_name
        }
        department_user_list.append(_t)
    return department_user_list


def update_department_users(department_id, user_id):
    try:
        user_id = json.loads(user_id)
    except Exception as e:
        g.error_code = 4000
        raise RuntimeError('Parameter error')

    # 判断部门是否存在
    if not db.department.get_department_by_id(department_id):
        g.error_code = 4000
        raise RuntimeError('Department information does not exist')

    # 获取 部门已存在的用户信息
    department_users = db.department_users.get_department_users_by_department_id(department_id)
    user_ids = [department.user_id for department in department_users]

    for u_id in user_id:
        if u_id in user_ids:
            user_ids.remove(u_id)
        else:
            db.department_users.create_department_user(department_id, u_id)

    if user_ids:
        for u_id in user_ids:
            db.department_users.delete_department_user_by_user_id(department_id, u_id)


def delete_department_user(department_id):
    db.department_users.delete_department_user_by_department_id(department_id)
