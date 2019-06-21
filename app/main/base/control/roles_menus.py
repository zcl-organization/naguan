# -*- coding:utf-8 -*-
import json

from app.main.base import db


def update_role(role_id, menu_id):
    # 获取role_id 角色 有权限的menu_id
    menu_id = json.loads(menu_id)

    # 判断角色是否是admin角色，admin拥有所有菜单权限，不允许修改权限
    role = db.role.list_by_id(role_id)
    if role.name == 'admin':
        raise Exception('It is not allowed to modify the menu permissions of the admin role.')

    menu_ids = db.roles_menus.get_menu_id_by_role_id(role_id)
    menu_id_list = [m_id.menu_id for m_id in menu_ids]

    for m_id in menu_id:
        if m_id in menu_id_list:
            menu_id_list.remove(m_id)
        else:
            db.roles_menus.create_menu_role(role_id, m_id)

    # 删除未在menu_id 上的菜单id
    if menu_id_list:
        for m_id in menu_id_list:
            db.roles_menus.delete_menu_role(role_id, m_id)


def get_menu_id_by_role_id(role_id):
    return db.roles_menus.get_menu_id_by_role_id(role_id)


def get_menu_id_by_role_list(role_list):
    menu_id = []
    for role_id in role_list:
        menu_ids = get_menu_id_by_role_id(role_id)

        menu_id_list = [menu.menu_id for menu in menu_ids]
        menu_id = menu_id + menu_id_list
    return list(set(menu_id))


def get_menu_by_role_id(role_id):
    menu_ids = get_menu_id_by_role_id(role_id)
    menu_id_list = [menu.menu_id for menu in menu_ids]
    return children_menu_list(menu_id_list)


def children_menu_list(menu_ids, parent_id=0):
    menu_level = db.menu.menu_list_by_parent_id(parent_id)
    if menu_level:
        menus = []
        for menu in menu_level:
            if menu.id in menu_ids:
                permission = True
            else:
                permission = False
            menu_level_children = children_menu_list(menu_ids, menu.id)
            menu_level_children_list = []
            if menu_level_children:

                for level_children in menu_level_children:
                    menu_level_children_list.append(level_children)

            menu_list = {
                'id': menu.id,
                'name': menu.name,
                'icon': menu.icon,
                'url': menu.url,
                'identifier': menu.identifier,
                'permission': permission
            }
            if menu_level_children_list:
                menu_list['menus'] = menu_level_children_list
            else:
                menu_list['menus'] = []
            menus.append(menu_list)
        return menus

    else:
        return None


def delete_role(role_id):
    # 判断用户角色是否是admin，admin不允许删除权限
    role = db.role.list_by_id(role_id)
    if role.name == 'admin':
        raise Exception('It is not allowed to delete the menu permission of the admin role.')
    db.roles_menus.delete_by_role_id(role_id)
