# -*- coding: utf-8 -*-
import unittest
from mock import Mock
from pyVmomi import vim

from app.main.base.control import cloud_platform
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.control.utils import get_connect, get_obj

platforms = [
    {
        'ip': '192.168.12.205', 
        'name': 'administrator@vsphere.local', 
        'password': 'Aiya@2018', 
        'port': '443'
    },
]
host_name = '192.168.12.203'
dc_name = 'Datacenter'
ds_name = 'datastore1'
cluster_name = 'gaf'

class TestVCenter(unittest.TestCase):
    def setUp(self):        
        cloud_platform.platform_list = Mock(return_value=platforms)
        self._vcenter = VCenter(1)
        self._si, self._connect, self._platform = get_connect(1)

    def test_get_si(self):
        self.assertEqual(self._si, self._vcenter.get_si())
    
    def test_get_connect(self):
        self.assertEqual(self._connect.about.instanceUuid, self._vcenter.get_connect().about.instanceUuid)

    def test_get_platform(self):
        self.assertEqual(self._platform, self._vcenter.get_platform())

    def test_find_hostsystem_by_name(self):
        test_host_obj = self._vcenter.find_hostsystem_by_name(host_name)
        right_host_obj = get_obj(self._connect, [vim.HostSystem], host_name)
        self.assertEqual(test_host_obj, right_host_obj)

    def test_find_datacenter_by_name(self):
        test_dc = self._vcenter.find_datacenter_by_name(dc_name)
        right_dc = get_obj(self._connect, [vim.Datacenter], dc_name)
        self.assertEqual(test_dc, right_dc)

    def test_find_data_store_by_name(self):
        test_ds = self._vcenter.find_datastore_by_name(ds_name)
        right_ds = get_obj(self._connect, [vim.Datastore], ds_name)
        self.assertEqual(test_ds, right_ds)

    def test_find_cluster_by_name(self):
        test_cluster = self._vcenter.find_cluster_by_name(cluster_name)
        right_cluster = get_obj(self._connect, [vim.ClusterComputeResource], cluster_name)
        self.assertEqual(test_cluster, right_cluster)


if __name__ == "__main__":
    unittest.main()
