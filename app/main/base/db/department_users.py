# -*- coding:utf-8 -*-
from flask import g

from app.models import DepartmentUsers, Department, Users, Company
from app.exts import db


def get_department_users(department_id, user_id):
    query = db.session.query(DepartmentUsers.id.label('department_user_id'),
                             DepartmentUsers.department_id.label('department_id'), Users.id.label('user_id'),
                             Users.username.label('user_name')).outerjoin(Users,
                                                                          DepartmentUsers.user_id == Users.id)
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


def get_department_users_by_user_id(user_id):
    return db.session.query(DepartmentUsers).filter_by(user_id=user_id).all()


def update_department_user_by_user_id(department_id, user_id, is_principal):
    department_user = db.session.query(DepartmentUsers).filter_by(department_id=department_id).filter_by(
        user_id=user_id).first()
    print(is_principal)
    department_user.is_principal = is_principal
    db.session.commit()


def get_department_users_by_company_id(company_id):
    query = db.session.query(DepartmentUsers.user_id).outerjoin(Department,
                                                                DepartmentUsers.department_id == Department.id)
    if company_id:
        query = query.filter(Department.company_id == company_id)
    return query.all()
