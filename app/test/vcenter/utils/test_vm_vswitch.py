import unittest
from mock import Mock

from app.main.base.control import cloud_platform
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_vswitch import VMVswitchManager

platforms = [
    {
        'ip': '192.168.12.205', 
        'name': 'administrator@vsphere.local', 
        'password': 'Aiya@2018', 
        'port': '443'
    },
]
host_name = '192.168.12.203'

num_port = 15
new_num_port = 128
mtu = 1500
nics = ['vmnic3',]
switch_name = 'Mu_Test'


class TestResourcePool(unittest.TestCase):
    def setUp(self):
        cloud_platform.platform_list = Mock(return_value=platforms)
        _vcenter = VCenter(1)
        host_system = _vcenter.find_hostsystem_by_name(host_name)
        self._vmvsm = VMVswitchManager(host_system)

    def test_create(self):
        self.assertTrue(self._vmvsm.create(switch_name, num_port, mtu, nics))

    def test_update(self):
        old = {'pnic': nics, 'mtu': mtu, 'num_ports': num_port}
        self.assertTrue(self._vmvsm.update(switch_name, old, number_of_ports=new_num_port))

    def test_destroy(self):
        self.assertTrue(self._vmvsm.destroy(switch_name))

    
if __name__ == "__main__":
    unittest.main()
