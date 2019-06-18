# -*- coding:utf-8 -*-

from app.main.base import db


def create_department(department_name, department_remarks, company_id, pid):
    """
    创建部门信息
    :param department_name:部门名称
    :param company_id:单位id
    :param pid:父级部门
    :return:
    """
    # 判断company_id 是否存在
    if not db.company.get_company_by_id(company_id):
        raise Exception('Company information does not exist')
    # 判断pid是否存在
    if pid:
        if not db.department.get_department_by_id(pid):
            raise Exception('The parent department does not exist')

    department = db.department.create_department(department_name, department_remarks, company_id, pid)
    department_list = []
    _t = {
        'department_id': department.id,
        'department_name': department.name,
        'department_pid': department.pid,
        'company_id': department.company_id,
    }
    department_list.append(_t)
    return department_list


def get_department(department_id, department_name, company_name):
    """
    获取部门信息
    :param department_id:
    :param department_name:
    :param company_name:
    :return:
    """
    departments = db.department.get_department(department_id, department_name, company_name)
    department_list = []
    for item in departments:
        _t = {
            'department_id': item.department_id,
            'department_name': item.department_name,
            'department_pid': item.department_pid,
            'department_status': item.department_status,
            'department_remarks': item.department_remarks,
            'company_id': item.company_id,
            'company_name': item.company_name
        }
        department_list.append(_t)
    return department_list


def update_department_by_id(department_id, department_name, department_remarks, department_status, department_pid):
    if not db.department.get_department_by_id(department_id):
        raise Exception('department information does not exist')
    db.department.update_department_by_id(department_id, department_name, department_remarks, department_status,
                                          department_pid)


def delete_department_by_id(department_id):
    """

    :param department_id:
    :return:
    """
    company = db.department.get_department_by_id(department_id)
    if not company:
        raise Exception('department information does not exist')

    db.department.delete_department_by_id(department_id)
