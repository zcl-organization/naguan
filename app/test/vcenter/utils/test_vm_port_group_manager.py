import unittest

import atexit
from pyVmomi import vim
from pyVim import connect
from app.main.vcenter.control.utils import get_obj, connect_server
from app.main.vcenter.utils.vm_port_group_manager import VMPortGroupManager

HOSTNAME = '192.168.12.203'
VSWITCH_NAME = 'vSwitch0'
PORTGROUP_NAME = 'test_group'


class TestVMPortGroupManager(unittest.TestCase):
    def setUp(self):
        platform = {'ip': '192.168.12.205', 'name': 'administrator@vsphere.local', 'password': 'Aiya@2018', 'port': '443'}
        si = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
        atexit.register(connect.Disconnect, si)
        content = si.RetrieveContent()
        host_system = get_obj(content, [vim.HostSystem], HOSTNAME)

        self._vpgm = VMPortGroupManager(host_system)

    def test_create(self):
        self.assertTrue(self._vpgm.create_port_group(VSWITCH_NAME, PORTGROUP_NAME))

    def test_des(self):
        self.assertTrue(self._vpgm.delete_port_group(PORTGROUP_NAME))


if __name__ == "__main__":
    unittest.main()
    