# -*- coding:utf-8 -*-

from app.main.base import db


def create_company(company_name, company_mobile, company_fax, principal_id, company_remarks):
    company = db.company.create_company(company_name, company_mobile, company_fax, principal_id, company_remarks)
    _t = {
        'company_id': company.id,
        'company_name': company.name,
        'company_mobile': company.mobile,
        'company_fax': company.fax,
        'company_remarks': company.remarks,
        'principal_id': company.principal_id
    }
    return _t


def get_company(company_id, name, principal_name):
    company = db.company.get_company(company_id, name, principal_name)

    company_list = []
    # print(company)
    for item in company:
        # print item.company_id
        _t = {
            'company_id': item.company_id,
            'company_name': item.company_name,
            'company_mobile': item.company_mobile,
            'company_fax': item.company_fax,
            'company_remarks': item.company_remarks,
            'principal_id': item.principal_id,
            'principal_name': item.principal_name
        }
        company_list.append(_t)
    return company_list


def update_company_by_id(company_id, company_name, company_mobile, company_fax, principal_id, company_remarks):
    # 判断是否存在company_id相关单位信息
    company = db.company.get_company_by_id(company_id)

    if not company:
        raise Exception('Company information does not exist')

    db.company.update_company_by_id(company_id, company_name, company_mobile, company_fax, principal_id,
                                    company_remarks)


def delete_company_by_id(company_id):
    company = db.company.get_company_by_id(company_id)
    if not company:
        raise Exception('Company information does not exist')

    db.company.delete_company_by_id(company_id)
