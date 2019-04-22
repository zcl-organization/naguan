# -*- coding:utf-8 -*-


class ExistsException(Exception):

    def __init__(self, msg, name=None):
        self.msg = msg
        self.name = name

    def __str__(self):
        return 'current ' + str(self.msg) + ' already exists: ' + str(self.name)

