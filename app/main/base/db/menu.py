# -*- coding:utf-8 -*-
from app.models import Menu
from app.exts import db


# 菜单列表
def menu_list(menu_id, url, name, identifier, all):
    query = db.session.query(Menu)
    if menu_id:
        query = query.filter_by(id=menu_id)
    if url:
        query = query.filter_by(url=url)
    if name:
        query = query.filter_by(name=name)
    if identifier:
        query = query.filter_by(identifier=identifier)
    # if options['limit'] and options['next_page']:
    #     query = query.paginate(page=options['next_page'], per_page=options['limit'], error_out=False)

    # result = query.items
    data = query.all()

    # data = []
    # for menu in result:
    #     menu_tmp = {
    #         'id': menu.id,
    #         'name': menu.name,
    #         'icon': menu.icon,
    #         'url': menu.url,
    #         'identifier': menu.identifier,
    #     }
    #     data.append(menu_tmp)

    # pg = {
    #     'has_next': query.has_next,
    #     'has_prev': query.has_prev,
    #     'page': query.page,
    #     'pages': query.pages,
    #     'size': options['limit'],
    #     'total': query.total
    #
    # }
    return data


# 创建菜单
def menu_create(icon, url, name, identifier, is_hide, is_hide_children, important, parent_id):
    try:
        new_menu = Menu()
        new_menu.icon = icon
        new_menu.url = url
        new_menu.name = name
        new_menu.identifier = identifier

        if is_hide == 1:
            new_menu.is_hide = True
        elif is_hide == 2:
            new_menu.is_hide = False
        else:
            raise Exception('is_hide_children information is incorrect, 1 is True, 2 is False')

        if is_hide_children == 1:
            new_menu.is_hide_children = True
        elif is_hide_children == 2:
            new_menu.is_hide_children = False
        else:
            raise Exception('is_hide_children information is incorrect, 1 is True, 2 is False')

        new_menu.important = important
        if parent_id:
            parent_menu = db.session.query(Menu).filter_by(id=parent_id).first()
            if parent_menu:
                new_menu.parent_id = parent_id
            else:
                new_menu.parent_id = 0
        else:
            new_menu.parent_id = 0

        db.session.add(new_menu)
        db.session.flush()
        db.session.commit()
        return new_menu

    except Exception as e:
        # print(e)
        raise Exception('Database operation exception')


# 根据id获取菜单信息
def menu_list_by_id(id):
    return db.session.query(Menu).filter_by(id=id).all()


# 是否存在子菜单
def children_menu_list(id):
    return db.session.query(Menu).filter_by(parent_id=id).all()


# 删除菜单
def menu_delete(id=None):
    query = db.session.query(Menu)
    menu_dellist = query.filter_by(id=id).first()
    db.session.delete(menu_dellist)
    db.session.commit()


def menu_update(id, icon, name, url, identifier, is_hide, is_hide_children, parent_id, important):
    try:
        menu = db.session.query(Menu).filter_by(id=id).first()

        # 判断是否更新状态
        # if menu:
        if icon:
            menu.icon = icon
        if name:
            menu.name = name
        if url:
            menu.url = url
        if identifier:
            menu.identifier = identifier

        if is_hide == 1:
            menu.is_hide = True
        elif is_hide == 2:
            menu.is_hide = False
        else:
            raise Exception('is_hide information is incorrect, 1 is True, 2 is False')

        if is_hide_children == 1:
            menu.is_hide_children = True
        elif is_hide_children == 2:
            menu.is_hide_children = False
        else:
            raise Exception('is_hide_children information is incorrect, 1 is True, 2 is False')

        if parent_id:
            menu.parent_id = parent_id
        if important:
            menu.important = important
        # db.session.add(menu)
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation exception')


# 根据父id获取菜单
def menu_list_by_parent_id(parent_id):
    return db.session.query(Menu).filter_by(parent_id=parent_id).all()
