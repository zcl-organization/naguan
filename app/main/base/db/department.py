# -*- coding:utf-8 -*-
from flask import g

from app.models import Department, Company
from app.exts import db


def get_department_by_id(department_id):
    return db.session.query(Department).filter_by(id=department_id).first()


def create_department(department_name, department_remarks, company_id, pid):
    new_department = Department()
    new_department.name = department_name
    new_department.company_id = company_id
    new_department.remarks = department_remarks
    new_department.pid = pid

    db.session.add(new_department)
    db.session.flush()
    try:
        db.session.commit()
    except Exception:
        raise Exception('Database operation exception')
    return new_department


def get_department(department_id, department_name, company_name):
    query = db.session.query(Department.id.label('department_id'), Department.name.label('department_name'),
                             Department.pid.label('department_pid'), Department.status.label('department_status'),
                             Department.remarks.label('department_remarks'), Company.id.label('company_id'),
                             Company.name.label('company_name')).outerjoin(Company,
                                                                           Company.id == Department.company_id)
    if department_id:
        query = query.filter(Department.id == department_id)
    if department_name:
        query = query.filter(Department.name == department_name)
    if company_name:
        query = query.filter(Company.name == company_name)

    return query.all()


def update_department_by_id(department_id, department_name, department_remarks, department_status,
                            department_pid):
    department = db.session.query(Department).filter_by(id=department_id).first()

    department.name = department_name
    department.remarks = department_remarks
    department.status = department_status
    department.pid = department_pid

    db.session.commit()


def delete_department_by_id(department_id):
    db.session.query(Department).filter_by(id=department_id).delete(synchronize_session=False)
    db.session.commit()
