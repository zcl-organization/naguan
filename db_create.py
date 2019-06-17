# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://naguna1:123456@192.168.12.108:3306/naguna1?charset=utf8'
# 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# 创建数据库的操作对象
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    # 给Role类创建一个uses属性，关联users表。
    # backref是反向的给User类创建一个role属性，关联roles表。这是flask特殊的属性。
    users = db.relationship('User', backref="role")

    # 相当于__str__方法。
    def __repr__(self):
        return "Role: %s %s" % (self.id, self.name)


class User(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是user。
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(32), unique=True)
    email2 = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(16))
    # 创建一个外键，和django不一样。flask需要指定具体的字段创建外键，不能根据类名创建外键
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "User: %s %s %s %s" % (self.id, self.name, self.password, self.role_id)


@app.route('/', methods=['post'])
def index():
    return 'the index page!'


if __name__ == '__main__':
    # 删除所有的表
    db.drop_all()
    # 创建表
    db.create_all()

    ro1 = Role(name="admin")
    # 先将ro1对象添加到会话中，可以回滚。
    db.session.add(ro1)

    ro2 = Role()
    ro2.name = 'user'
    print(ro2.name)
    db.session.add(ro2)

    # 最后插入完数据一定要提交
    db.session.commit()
