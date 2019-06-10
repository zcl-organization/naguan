# -*- coding:utf-8 -*-

from app.models import RolesMenus
from app.exts import db


def create_menu_role(role_id, menu_id):
    new_role_menu = RolesMenus()
    new_role_menu.role_id = role_id
    new_role_menu.menu_id = menu_id
    try:
        db.session.add(new_role_menu)
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation failed')


def get_menu_id_by_role_id(role_id):
    return db.session.query(RolesMenus.menu_id).filter_by(role_id=role_id).all()


def delete_menu_role(role_id, menu_id):
    query = db.session.query(RolesMenus)
    query.filter_by(role_id=role_id).filter_by(menu_id=menu_id).delete(synchronize_session=False)
    db.session.commit()


def delete_by_menu_id(menu_id):
    query = db.session.query(RolesMenus)
    query.filter_by(menu_id=menu_id).delete(synchronize_session=False)
    db.session.commit()


def delete_by_role_id(role_id):
    query = db.session.query(RolesMenus)
    query.filter_by(role_id=role_id).delete(synchronize_session=False)
    db.session.commit()
