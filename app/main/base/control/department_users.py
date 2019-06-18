# -*- coding:utf-8 -*-

from app.main.base import db
import json


def get_department_users(department_id, user_id):
    department_users = db.department_users.get_department_users(department_id, user_id)

    return department_users


def update_department_users(department_id, user_id):
    try:
        user_id = json.loads(user_id)
    except Exception as e:
        raise RuntimeError('Parameter error')

    # 获取 部门已存在的用户信息
    department_users = db.department_users.get_department_users_by_department_id(department_id)
    user_ids = [department.user_id for department in department_users]

    for u_id in user_id:
        if u_id in user_ids:
            department_users.remove(u_id)
        else:
            db.department_users.create_department_user(department_id, u_id)

    if user_ids:
        for u_id in user_ids:
            db.department_users.delete_department_user_by_user_id(department_id, u_id)


def delete_department_user(department_id):
    db.department_users.delete_department_user_by_department_id(department_id)