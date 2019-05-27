# -*- coding: utf-8 -*
from enum import Enum, unique

@unique
class Code(Enum):
    # 登录
    LoginSuccess = {"1000": "登录成功"}
    LoginParameterErr = {"1001": "用户名或者密码错误"}

    # 用户管理
