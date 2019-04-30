# -*- coding:utf-8 -*-
import datetime

from app.models import Users
from app.exts import db


# 根据条件获取用户信息
def user_list(user_id, email, mobile, remarks, next_page, limit):
    try:
        query = db.session.query(Users).filter_by(is_deleted=0)
        if user_id:
            query = query.filter_by(id=user_id)
        if email:
            query = query.filter_by(email=email)
        if mobile:
            query = query.filter_by(mobile=mobile)
        if remarks:
            query = query.filter_by(remarks=remarks)
        if next_page and limit:
            query = query.paginate(page=next_page, per_page=limit, error_out=False)

        result = query.items
    except Exception as e:
        raise Exception('Database query is abnormal')

    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'size': limit,
        'total': query.total
    }
    return result, pg


# 根据用户名称获取用户信息
def user_list_by_name(username):
    if username:
        try:
            data = db.session.query(Users).filter_by(username=username).filter_by(is_deleted=0).first()
        except Exception as e:
            raise Exception('Database query is abnormal')
        return data
    else:
        raise Exception('Parameter error')


# 根据邮箱地址获取用户信息
def user_list_by_email(email):
    return db.session.query(Users).filter_by(email=email).filter_by(is_deleted=0).first()


# 根据id获取用户信息
def user_list_by_id(id):
    return db.session.query(Users).filter_by(id=id).filter_by(is_deleted=0).first()


# 创建用户信息
def user_create(username, password, email, first_name, uid, mobile, department, job, location, company, sex, uac,
                active, is_superuser, remarks, current_login_ip):
    # query = db.session.query(Users)
    print(email)
    newuser = Users()
    newuser.username = username
    # newuser.password = args['password']
    newuser.hash_password(password)
    newuser.email = email
    newuser.first_name = first_name
    newuser.uid = uid
    newuser.mobile = mobile
    newuser.department = department
    newuser.job = job
    newuser.location = location
    newuser.company = company
    newuser.sex = sex
    newuser.uac = uac
    # newuser.active = args['active']
    newuser.active = True
    # newuser.is_superuser = args['is_superuser']
    newuser.last_login_ip = current_login_ip
    newuser.current_login_ip = current_login_ip
    newuser.login_count = 0
    newuser.is_superuser = True
    newuser.remarks = remarks
    try:
        db.session.add(newuser)
        db.session.commit()
    except Exception, e:
        raise Exception('User information creation failed')


# 根据id删除用户信息
def user_delete(id=None):
    query = db.session.query(Users)
    try:
        user_willdel = query.filter_by(id=id).first()
        # db.session.delete(user_willdel)
        user_willdel.is_deleted = id
        user_willdel.deleted_at = datetime.datetime.now()
        db.session.commit()
    except Exception as e:
        raise Exception('User information delete failed')


# 根据id更新用户信息
def user_update(id, active, username, password, mobile, company, department, remarks):
    user = db.session.query(Users).filter_by(id=id).first()
    # 判断是否更新状态
    # print(options)
    if active:

        # user.active = options['active']
        if active == 1:
            user.active = True
        elif active == 2:
            user.active = False
        else:
            # return False
            raise Exception('Parameter error')
    # 判断是否更新密码
    if password:
        user.password = Users.get_hash_password(password)
    if username:
        user.username = username
    if mobile:
        user.mobile = mobile
    if company:
        user.company = company
    if department:
        user.department = department
    if remarks:
        user.remarks = remarks
    try:
        db.session.commit()
    except Exception as e:
        raise Exception('Database update exception')


def update_login_time(user):
    user.login_count += 1
    user.last_login_at = user.current_login_at
    user.current_login_at = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
