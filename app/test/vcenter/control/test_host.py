# -*- coding=utf-8 -*-
import time
import unittest
from mock import Mock
from pyVmomi import vim

from app.main.base.control import cloud_platform
from app.main.vcenter import db
from app.main.vcenter.control.host import Host
from app.main.vcenter.control.utils import get_obj
from app.main.vcenter.utils.base import VCenter
from manage import app

esxi_hostname = '192.168.78.59'
esxi_username = 'root'
esxi_password = 'Kpy@2019'
platforms = [{'ip': '192.168.78.205',
              'name': 'linjq@vsphere.local',
              'password': 'Aiya@2018',
              'port': '443',
              'id': 1}]


class cluster():
    mor_name = 'domain-c101'


class vcenter_tree_cluster():
    type = 3


class host():
    name = '192.168.78.59'


class VCenterHost(unittest.TestCase):
    def setUp(self):
        db.host.get_host_by_name = Mock(return_value='')
        db.clusters.get_cluster = Mock(return_value=cluster())
        db.vcenter.get_vcenter_obj_by_mor_name = Mock(return_value=vcenter_tree_cluster())
        cloud_platform.platform_list = Mock(return_value=platforms)
        self._vCenter = Mock(return_value=platforms)
        self._host = Host(1)
        db.vcenter.vcenter_tree_del_by_mor_name = Mock(return_value='')

    def tearDown(self):
        pass

    def test_add_host(self):
        with app.test_request_context():
            self._host.add_host(esxi_hostname, esxi_username, esxi_password)
        self.assertEqual(esxi_hostname, get_obj(VCenter(1).connect, [vim.HostSystem], esxi_hostname).name)

    def test_remove_host(self):
        pass


if __name__ == "__main__":
    unittest.main()
