# -*- coding:utf-8 -*-
from flask import g

from app.main.base import db
from app.main.base.control import roles_users as role_user_manage
from app.main.base.control import roles_menus as role_menu_manage


# 获取菜单列表
def menu_list(menu_id, url, name, identifier, all):
    # 获取当前用户角色id
    role_list = role_user_manage.get_current_roles_id()
    role_id_list = [role.role_id for role in role_list]
    # print(role_id_list)
    # 获取当前用户角色所拥有的菜单
    menu_ids = role_menu_manage.get_menu_id_by_role_list(role_id_list)
    # print(menu_ids)
    if all:
        result = db.menu.menu_list(menu_id, url, name, identifier, all)
        data = []
        for menu in result:
            menu_tmp = {
                'id': menu.id,
                'name': menu.name,
                'icon': menu.icon,
                'url': menu.url,
                'identifier': menu.identifier,
            }
            data.append(menu_tmp)
        return data
    else:
        return children_menu_list(menu_ids)


# 递归获取所有子菜单
def children_menu_list(menu_ids, parent_id=0):
    menu_level = db.menu.menu_list_by_parent_id(parent_id)
    if menu_level:
        menus = []
        for menu in menu_level:
            if menu.id in menu_ids:
                menu_level_2 = children_menu_list(menu_ids, menu.id)
                menu_level_2_list = []
                if menu_level_2:

                    for level_2 in menu_level_2:
                        menu_level_2_list.append(level_2)

                menu_list = {
                    'id': menu.id,
                    'name': menu.name,
                    'icon': menu.icon,
                    'url': menu.url,
                    'identifier': menu.identifier,
                }
                if menu_level_2_list:
                    menu_list['menus'] = menu_level_2_list
                else:
                    menu_list['menus'] = []
                menus.append(menu_list)
        return menus

    else:
        return None


# 创建菜单信息
# def menu_create(options=None):
def menu_create(icon, url, name, identifier, is_hide, is_hide_children, important, parent_id):
    data = db.menu.menu_create(icon, url, name, identifier, is_hide, is_hide_children, important, parent_id)

    menu_dict = {
        'id': data.id,
        'name': data.name,
        'icon': data.icon,
        'url': data.url,
        'identifier': data.identifier,
    }

    # 获取admin角色id
    admin_role = db.role.get_role_id_by_name('admin')
    # 为admin角色分配权限
    db.roles_menus.create_menu_role(admin_role.id, data.id)
    return [menu_dict]


# 判断是否有子菜单
def children_menu(id=None):
    return db.menu.children_menu_list(id)


# 删除菜单信息
def menu_delete(id=None):
    # 判断是否有菜单
    try:
        menu = db.menu.menu_list_by_id(id)
        # print(menu)
        if menu:
            sub_menu = db.menu.children_menu_list(id)
            # print(children_menu)
            if sub_menu:
                g.error_code = 1211
                raise Exception('Menu deletion failed, submenu exists')
            else:
                # 删除当前菜单 权限相关的角色信息
                db.roles_menus.delete_by_menu_id(id)
                return db.menu.menu_delete(id)
        else:
            g.error_code = 1212
            raise Exception('No current menu exists')
    except Exception as e:
        g.error_code = 1213
        raise Exception(e)


# 更新菜单信息
def menu_update(id, icon, name, url, identifier, is_hide, is_hide_children, parent_id, important):
    # 判断是否有菜单

    menu = db.menu.menu_list_by_id(id)
    if menu:
        # 更新用户信息
        return db.menu.menu_update(id, icon, name, url, identifier, is_hide, is_hide_children, parent_id, important)
    else:
        g.error_code = 1223
        raise Exception('No current menu exists')
