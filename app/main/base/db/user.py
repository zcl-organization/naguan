# -*- coding:utf-8 -*-
from app.models import Users
from app.exts import db


# 根据条件获取用户信息
def user_list(options=None):
    query = db.session.query(Users)

    if options.get('id'):
        query = query.filter_by(id=options.get('id'))
    if options.get('email'):
        query = query.filter_by(email=options.get('email'))
    if options.get('mobile'):
        query = query.filter_by(mobile=options.get('mobile'))
    if options.get('remarks'):
        query = query.filter_by(remarks=options.get('remarks'))
    if options.get('limit') and options.get('next_page'):
        query = query.paginate(page=options.get('next_page'), per_page=options.get('limit'), error_out=False)
    # print(query)
    result = query.items

    # has_next = query.has_next
    # has_prev = query.has_prev

    # print(dir(query))
    userinfo = []
    for user in result:
        user = {
            'name': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'uid': user.uid,
            'id': user.id,
            'mobile': user.mobile,
            'department': user.department,
            'job': user.job,
            'location': user.location,
            'company': user.company,
            'sex': user.sex,
            'uac': user.uac,
            'date_created': user.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_at': user.last_login_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_ip': user.last_login_ip,
            'current_login_ip': user.current_login_ip,
            'login_count': user.login_count
        }
        userinfo.append(user)

    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'size': options['limit'],
        'total': query.total

    }
    return userinfo, pg


# 根据用户名称获取用户信息
def user_list_by_name(username):
    # print('username:', username)
    if username:
        data = db.session.query(Users).filter_by(username=username).all()
        # print(data)
        return data
    else:
        return -1


# 根据邮箱地址获取用户信息
def user_list_by_email(email):
    # if email:

    return db.session.query(Users).filter_by(email=email).all()


# 根据id获取用户信息
def user_list_by_id(id):
    return db.session.query(Users).filter_by(id=id).first()


# 创建用户信息
def user_create(options=None):
    query = db.session.query(Users)
    newuser = Users()
    newuser.username = options['username']
    # newuser.password = args['password']
    newuser.hash_password(options['password'])
    newuser.email = options['email']
    newuser.first_name = options['first_name']
    newuser.uid = options['uid']
    newuser.mobile = options['mobile']
    newuser.department = options['department']
    newuser.job = options['job']
    newuser.location = options['location']
    newuser.company = options['company']
    newuser.sex = options['sex']
    newuser.uac = options['uac']
    # newuser.active = args['active']
    newuser.active = True
    # newuser.is_superuser = args['is_superuser']
    newuser.last_login_ip = options['current_login_ip']
    newuser.current_login_ip = options['current_login_ip']
    newuser.login_count = 0
    newuser.is_superuser = True
    newuser.remarks = options['remarks']
    try:
        db.session.add(newuser)
        db.session.commit()
    except Exception, e:
        return False
    return True


# 根据id删除用户信息
def user_delete(id=None):
    query = db.session.query(Users)
    user_willdel = query.filter_by(id=id).first()
    db.session.delete(user_willdel)
    db.session.commit()
    return True


# 根据id更新用户信息
def user_update(id, options):
    user = db.session.query(Users).filter_by(id=id).first()
    # 判断是否更新状态
    # print(options)
    if options['active']:

        # user.active = options['active']
        if options['active'] == 1:
            user.active = True
        elif options['active'] == 2:
            user.active = False
        else:
            return False

    # 判断是否更新密码
    if options['password']:
        user.password = Users.get_hash_password(options['password'])
    if options['username']:
        user.username = options['username']
    if options['mobile']:
        user.mobile = options['mobile']
    if options['company']:
        user.company = options['company']
    if options['department']:
        user.department = options['department']
    if options['remarks']:
        user.remarks = options['remarks']

    db.session.commit()
    return True

