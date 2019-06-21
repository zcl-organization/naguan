import unittest
from mock import Mock

from pyVmomi import vim

from app.main.base.control import cloud_platform
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_resource_pool import VMResourcePoolManager
from app.main.vcenter.control.utils import get_mor_name

platforms = [
    {
        'ip': '192.168.78.205', 
        'name': 'administrator@vsphere.local', 
        'password': 'Aiya@2018', 
        'port': '443'
    },
]
rp_name = 'test_rp'
cluster_name = 'cluster2' #'192.168.78.203' # 'gaf'


class TestResourcePool(unittest.TestCase):
    def setUp(self):
        cloud_platform.platform_list = Mock(return_value=platforms)
        _vcenter = VCenter(1)
        cluster = _vcenter.find_cluster_by_name(cluster_name)
        self._vmrpm = VMResourcePoolManager(cluster)

    def test_create(self):
        self.assertTrue(self._vmrpm.create(rp_name))

    def test_destroy(self):
        resource_pools = [item for item in self._vmrpm._cluster.resourcePool.resourcePool]

        d_name = rp_name
        for item in resource_pools:
            if isinstance(item, vim.ResourcePool):
                if item.name == rp_name:
                    d_name = get_mor_name(item)
                    break
                if item.resourcePool:
                    resource_pools.extend(item.resourcePool)

        self.assertTrue(self._vmrpm.destroy(d_name))

    
if __name__ == "__main__":
    unittest.main()
