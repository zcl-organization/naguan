# -*- coding:utf-8 -*-
from flask import g

from app.models import DepartmentUsers, Department, Users, Company
from app.exts import db


def get_department_users(department_id, user_id):
    query = db.session.query(DepartmentUsers.id, DepartmentUsers.department_id, Users.id,
                             Users.username).outjoin(DepartmentUsers, DepartmentUsers.user_id == Users.id)
    if department_id:
        query = query.filter(DepartmentUsers.department_id == department_id)
    # if department_name:
    #     query = query.filter(Department.id == department_id)
    if user_id:
        query = query.filter(Users.id == user_id)

    return query.all()


def get_department_users_by_department_id(department_id):
    return db.session.query(DepartmentUsers).filter_by(department_id=department_id).all()


def create_department_user(department_id, user_id):
    new_department_user = DepartmentUsers()
    new_department_user.department_id = department_id
    new_department_user.user_id = user_id
    db.session.add(new_department_user)
    db.session.commit()


def delete_department_user_by_user_id(department_id, user_id):
    db.session.query(DepartmentUsers).filter_by(department_id=department_id).filter_by(user_id=user_id).delete(
        synchronize_session=False)
    db.session.commit()


def delete_department_user_by_department_id(department_id):
    db.session.query(DepartmentUsers).filter_by(department_id=department_id).delete(synchronize_session=False)
    db.session.commit()
