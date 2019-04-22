# -*- coding:utf-8 -*-
from app.main.base.db import menu as db_menu


# 获取菜单列表
def menu_list(options=None):
    if options['id'] or options['url'] or options['name'] or options['identifier'] or options['all']:
        print('all')
        return db_menu.menu_list(options)
    else:
        return childer_menu_list(0)


# 递归获取所有子菜单
def childer_menu_list(parent_id=0):

    menu_level = db_menu.menu_list_by_parent_id(parent_id)
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
def menu_create(options=None):
    return db_menu.menu_create(options)


# 判断是否有子菜单
def children_menu(id=None):
    return db_menu.children_menu_list(id)


# 删除菜单信息
def menu_delete(id=None):
    # 判断是否有菜单
    menu = db_menu.menu_list_by_id(id)
    if menu:
        children_menu = db_menu.children_menu_list(id)
        if children_menu:
            return menu
        else:
            db_menu.menu_delete(id)
            return menu
    else:
        return False


# 更新菜单信息
def menu_update(id, options=None):
    # 判断是否有菜单
    menu = db_menu.menu_list_by_id(id)
    if menu:
        # 更新用户信息
        return db_menu.menu_update(id, options)
    else:
        return False