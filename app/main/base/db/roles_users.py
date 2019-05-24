# -*- coding:utf-8 -*-

from app.models import RolesUsers, Users, Roles
from app.exts import db


def roles_users_list(user_name, role_name):
    query = db.session.query(Users.id.label('user_id'), Users.first_name.label('user_name'),
                             Roles.name.label('role_name'), Roles.id.label('role_id')).filter(
        Users.id == RolesUsers.user_id).filter(Roles.id == RolesUsers.role_id)
    # 根据用户名 角色名查询
    if user_name:
        query = query.filter(Users.first_name == user_name)
    if role_name:
        query = query.filter(Roles.name == role_name)

    result = query.all()
    return result


def role_user_list_by_id(user_id):
    query = db.session.query(RolesUsers).filter(RolesUsers.user_id == user_id)

    return query.all()


# 获取资源id
def get_roles_users(user_id=None, role_id=None):
    if user_id:
        roles_users = db.session.query(RolesUsers).filter_by(user_id=user_id).\
            filter_by(role_id=role_id).first()
    else:
        roles_users = db.session.query(RolesUsers).order_by(-RolesUsers.id).first()
    roles_users_id = roles_users.id
    return roles_users_id
#
