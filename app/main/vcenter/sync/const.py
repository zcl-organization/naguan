# -*- coding: utf-8 -*-
from enum import Enum


class SyncOperation(Enum):
    """
    同步操作类型
    """
    PLATFORM = 1
    DATACENTER = 2
    PORTGROUP = 3
    DVSWITCH = 4
    DATASTORE = 5
    CLUSTER = 6
    RESOURCEPOOL = 7
    HOST = 8
    VSWITCH = 9
    VM = 10


class PlatformType(Enum):
    """
    Tree表类型
    """
    PLATFROM = 1
    DATACENTER = 2
    CLUSTER = 3
    HOST = 4
    RESOURCEPOOL = 5
