# -*- coding: utf-8 -*-
# Example of combining Flask-Security and Flask-Admin.


# Uses Flask-Security to control access to the application, with "admin" and "end-user" roles.
# Uses Flask-Admin to provide an admin UI for the lists of users and roles.
# SQLAlchemy ORM, Flask-Mail and WTForms are used in supporting roles, as well.
import datetime
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils, login_user, roles_accepted

from app.common import set_unauth_view
# from flask_mail import Mail
# from flask.ext.admin import Admin
# from flask.ext.admin.contrib import sqla

from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import os

# Initialize Flask and set some config values
app = Flask(__name__, template_folder='app/templates')
app.config['DEBUG'] = True
# Replace this with your own secret key
app.config['SECRET_KEY'] = 'super-secret'
# The database must exist (although it's fine if it's empty) before you attempt to access any page of the app
# in your browser.
# I used a PostgreSQL database, but you could use another type of database, including an in-memory SQLite database.
# You'll need to connect as a user with sufficient privileges to create tables and read and write to them.
# Replace this with your own database connection string.
# xxxxx
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aaaaaa@192.168.125.160:3306/Code3?charset=utf8'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'develop.db')
# Set config values for Flask-Security.
# We're using PBKDF2 with salt.
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# Replace this with your own salt.
app.config[
    'SECURITY_PASSWORD_SALT'] = 'xxxxxxxxxxxxxxxxxxxxx'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECURITY_UNAUTHORIZED_VIEW'] = 'index'

# Flask-Security optionally sends email notification to users upon registration, password reset, etc.
# It uses Flask-Mail behind the scenes.
# Set mail-related config values.
# Replace this with your own "from" address


db = SQLAlchemy(app)

# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired('accountNumber is null')])
    password = PasswordField('password', validators=[DataRequired('password is null')])


# Role class
class Role(db.Model, RoleMixin):
    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


# User class
class User(db.Model, UserMixin):
    # Our User has six fields: ID, email, password, active, confirmed_at and roles. The roles field represents a
    # many-to-many relationship using the roles_users table. Each user may have no role, one role, or multiple roles.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    uid = db.Column(db.String(20), nullable=False, default='')
    mobile = db.Column(db.String(30), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(3), nullable=False)
    uac = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.utcnow())
    confirmed_at = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.utcnow())

    last_login_at = db.Column(db.DateTime, nullable=False,
                              default=lambda: datetime.datetime.utcnow())
    current_login_at = db.Column(db.DateTime, nullable=False,
                                 default=lambda: datetime.datetime.utcnow())
    last_login_ip = db.Column(db.String(45), nullable=False)
    current_login_ip = db.Column(db.String(45), nullable=False)
    login_count = db.Column(db.Integer, nullable=False)

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )


# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Executes before the first request is processed.
@app.before_first_request
def before_first_request():
    # Create any database tables that don't exist yet.
    db.create_all()
    print('first_login')
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='End user')

    user_datastore.find_or_create_role(name='special-edit', description='Special user edit')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('test@qq.com'):
        user_datastore.create_user(email='test@qq.com', password='xxxxx', first_name='z', username='test', uid='1',
                                   mobile='1111111', department='11111', job='it', location='111', company='kpy',
                                   sex='boy', uac=1, active=True, is_superuser=True, last_login_ip='123.111.33.4',
                                   current_login_ip='111.111.222.222', login_count=0)
    if not user_datastore.get_user('admin@qq.com'):
        user_datastore.create_user(email='admin@qq.com', password='xxxxx', first_name='c', username='t2est', uid='1',
                                   mobile='1111111', department='11111', job='it', location='111', company='kpy',
                                   sex='boy', uac=1, active=True, is_superuser=True, last_login_ip='123.111.33.4',
                                   current_login_ip='111.111.222.222', login_count=0)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('test@qq.com', 'user')
    user_datastore.add_role_to_user('admin@qq.com', 'admin')

    user_datastore.add_role_to_user('test@qq.com', 'special-edit')
    db.session.commit()

    users = User.query.filter_by(email='admin@qq.com').first()
    # cur_user = User()
    # cur_user.id = users.id

    login_user(users)


@app.before_request
def before_request():
    print('is_active:', current_user.is_active)
    if current_user.has_role('admin'):
        print('current+user:', current_user)
        pass
    else:
        print(current_user.is_active)


@app.route('/unauth', endpoint='unauth')
def unauth():
    return 'unauth'


# Displays the home page.
@app.route('/', endpoint='index')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
# @roles_accepted('admin')
# @login_required
def index():
    form = LoginForm()
    # return 'cccc'
    return render_template('test.html', form=form)


@app.route('/admin', endpoint='admin')
# @set_unauth_view('User')
# @roles_accepted('admin')
def admin():
    # "管理员界面"
    print('管理员界面')
    print(current_user.has_role('admin'))
    return 'admin view'


@app.route('/log', endpoint='log', methods=['post'])
# @roles_accepted('user', 'admin')
def log():
    form = LoginForm()
    email = form.email.data
    password = form.password.data

    # 暂时不做密码验证
    users = User.query.filter_by(email=email).first()
    print(users)
    if users:
        cur_user = User()
        cur_user.id = users.id
        # print('user_id:', users.id)
        login_user(users)
        # print('url 重定向 到admin 视图')
        return redirect('/admin')
    else:
        return redirect('/')


@app.route('/test')
# @roles_accepted('user', 'admin')
# @set_unauth_view('unauth')
def test():
    return 'test'


@app.route('/user', endpoint='User')
# @roles_accepted('User', 'admin')
# @set_unauth_view('/')
def user():
    return 'user'


@app.route('/edit')
@roles_accepted('admin', 'special-edit')
def edit():
    return 'edit something'


# If running locally, listen on all IP addresses, port 8080
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int('8080'),
        debug=app.config['DEBUG']
    )
