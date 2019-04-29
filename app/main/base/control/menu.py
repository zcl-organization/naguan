# -*- coding:utf-8 -*-
# from app.main.base.db import menu as db_menu
from app.main.base import db


# 获取菜单列表
def menu_list(menu_id, url, name, identifier, all):
    if menu_id or url or name or identifier or all:

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
        return childer_menu_list(0)


# 递归获取所有子菜单
def childer_menu_list(parent_id=0):
    menu_level = db.menu.menu_list_by_parent_id(parent_id)
    if menu_level:

        menus = []
        # childer_menus =[]

        for menu in menu_level:
            menu_level_2 = childer_menu_list(menu.id)
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
    return db.menu.menu_create(icon, url, name, identifier, is_hide, is_hide_children, important, parent_id)


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
                raise Exception('Menu deletion failed, submenu exists')
            else:
                db.menu.menu_delete(id)
        else:
            raise Exception('No current menu exists')
    except Exception as e:
        raise Exception(e)


# 更新菜单信息
def menu_update(id, icon, name, url, identifier, is_hide, is_hide_children, parent_id, important):
    # 判断是否有菜单

    menu = db.menu.menu_list_by_id(id)
    if menu:
        # 更新用户信息
        return db.menu.menu_update(id, icon, name, url, identifier, is_hide, is_hide_children, parent_id, important)
    else:
        raise Exception('No current menu exists')
