import unittest
from mock import Mock

from app.main.base.control import cloud_platform
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_resource_pool import VMResourcePoolManager

platforms = [
    {
        'ip': '192.168.12.205', 
        'name': 'administrator@vsphere.local', 
        'password': 'Aiya@2018', 
        'port': '443'
    },
]
rp_name = 'test_rp'
cluster_name = 'gaf'


class TestResourcePool(unittest.TestCase):
    def setUp(self):
        cloud_platform.platform_list = Mock(return_value=platforms)
        _vcenter = VCenter(1)
        cluster = _vcenter.find_cluster_by_name(cluster_name)
        self._vmrpm = VMResourcePoolManager(cluster)

    def test_create(self):
        self.assertTrue(self._vmrpm.create(rp_name))

    def test_destroy(self):
        self.assertTrue(self._vmrpm.destroy(rp_name))

    
if __name__ == "__main__":
    unittest.main()
