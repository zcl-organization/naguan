# -*- coding:utf-8 -*-
from flask import g

from app.models import Company, Users
from app.exts import db


def create_company(name, mobile, fax, principal_id, remarks):
    new_company = Company()
    new_company.name = name
    new_company.mobile = mobile
    new_company.fax = fax
    new_company.principal_id = principal_id
    new_company.remarks = remarks
    db.session.add(new_company)
    try:
        db.session.flush()
        db.session.commit()
        return new_company
    except Exception as e:
        raise Exception('Database operation exception')


def get_company(company_id, name, principal_name):
    query = db.session.query(Company.id.label('company_id'), Company.name.label('company_name'),
                             Company.mobile.label('company_mobile'), Company.fax.label('company_fax'),
                             Company.remarks.label('company_remarks'), Users.id.label('principal_id'),
                             Users.username.label('principal_name')).outerjoin(Users, Users.id == Company.principal_id)
    if company_id:
        query = query.filter(Company.id == company_id)
    if name:
        query = query.filter(Company.name == name)
    if principal_name:
        query = query.filter(Users.username == principal_name)

    return query.all()


def get_company_by_id(company_id):
    return db.session.query(Company).filter_by(id=company_id).first()


def update_company_by_id(company_id, name, mobile, fax, principal_id,remarks):
    company = db.session.query(Company).filter_by(id=company_id).first()
    if name:
        company.name = name
    if mobile:
        company.mobile = mobile
    if fax:
        company.fax = fax
    if principal_id:
        company.principal_id = principal_id
    if remarks:
        company.remarks = remarks
    try:
        db.session.commit()
        return company
    except Exception as e:
        raise Exception('Database operation failed')


def delete_company_by_id(company_id):
    db.session.query(Company).filter_by(id=company_id).delete(synchronize_session=False)
    db.session.commit()
