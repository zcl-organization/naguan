# -*- coding:utf-8 -*-
from app.models import Menu
from app.exts import db


# 菜单列表
def menu_list(options=None):
    query = db.session.query(Menu)
    if options['id']:
        query = query.filter_by(id=options['id'])
    if options['url']:
        query = query.filter_by(url=options['url'])
    if options['name']:
        query = query.filter_by(name=options['name'])
    if options['identifier']:
        query = query.filter_by(identifier=options['identifier'])
    if options['limit'] and options['next_page']:
        query = query.paginate(page=options['next_page'], per_page=options['limit'], error_out=False)

    # result = query.items
    result = query.all()
    print(result)
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
def menu_create(options=None):
    new_menu = Menu()
    new_menu.icon = options['icon']
    new_menu.url = options['url']
    new_menu.name = options['name']
    new_menu.identifier = options['identifier']

    if options['is_hide'] == 1:
        new_menu.is_hide = True
    elif options['is_hide'] == 2:
        new_menu.is_hide = False
    else:
        print('is_hide')
        return False

    if options['is_hide_children'] == 1:
        new_menu.is_hide_children = True
    elif options['is_hide_children'] == 2:
        new_menu.is_hide_children = False
    else:
        print('is_hide_children')
        return False

    # new_menu.is_hide = False
    # new_menu.is_hide_children = False
    new_menu.important = options['important']
    if options['parent_id']:
        parent_menu = db.session.query(Menu).filter_by(id=options['parent_id']).first()
        if parent_menu:
            new_menu.parent_id = options['parent_id']
        else:
            new_menu.parent_id = 0
    else:
        new_menu.parent_id = 0
    try:
        db.session.add(new_menu)
        db.session.commit()
    except Exception, e:
        return False
    return options


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


def menu_update(id, options):
    menu = db.session.query(Menu).filter_by(id=id).first()

    # 判断是否更新状态
    # if menu:
    if options['icon']:
        menu.icon = options['icon']
    if options['name']:
        menu.name = options['name']
    if options['url']:
        menu.url = options['url']
    if options['identifier']:
        menu.identifier = options['identifier']

    if options['is_hide'] == 1:
        # print('is_hide 1')
        menu.is_hide = True
    elif options['is_hide'] == 2:
        # print('is_hide 1')
        menu.is_hide = False
    else:
        # print('is_hide', options['is_hide'])
        return False

    if options['is_hide_children'] == 1:
        menu.is_hide_children = True
    elif options['is_hide_children'] == 2:
        menu.is_hide_children = False
    else:
        return False

    # if options['is_hide']:
    #     menu.is_hide = options['is_hide']
    # if options['is_hide_children']:
    #     menu.is_hide_children = options['is_hide_children']
    if options['parent_id']:
        menu.parent_id = options['parent_id']
    if options['important']:
        menu.important = options['important']
    # db.session.add(menu)
    db.session.commit()
    # print('update')
    return options


# 根据父id获取菜单
def menu_list_by_parent_id(parent_id):
    return db.session.query(Menu).filter_by(parent_id=parent_id).all()

