import unittest

import atexit
from pyVmomi import vim
from pyVim import connect
from app.main.vcenter.control.utils import get_obj, connect_server
from app.main.vcenter.utils.vm_port_group_manager import VMPortGroupManager
from app.main.vcenter.utils.vm_port_group_manager import VMDvsPortGroupManager

HOSTNAME = '192.168.78.203'
VSWITCH_NAME = 'vSwitch0'
PORTGROUP_NAME = 'test_group'
DVSWITCH_NAME = 'DSwitch-test'
NUM_PORT = 4


class TestVMPortGroupManager(unittest.TestCase):
    def setUp(self):
        platform = {'ip': '192.168.78.205', 'name': 'administrator@vsphere.local', 'password': 'Aiya@2018', 'port': '443'}
        si = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
        atexit.register(connect.Disconnect, si)
        content = si.RetrieveContent()
        host_system = get_obj(content, [vim.HostSystem], HOSTNAME)

        self._vpgm = VMPortGroupManager(host_system)

    def test_create(self):
        self.assertTrue(self._vpgm.create_port_group(VSWITCH_NAME, PORTGROUP_NAME))

    def test_destroy(self):
        self.assertTrue(self._vpgm.delete_port_group(PORTGROUP_NAME))


class TestVMDvsPortGroupManager(unittest.TestCase):
    def setUp(self):
        platform = {'ip': '192.168.78.205', 'name': 'administrator@vsphere.local', 'password': 'Aiya@2018', 'port': '443'}
        si = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
        atexit.register(connect.Disconnect, si)
        content = si.RetrieveContent()
        dv_switch = get_obj(content, [vim.DistributedVirtualSwitch], DVSWITCH_NAME)

        self._vdpgm = VMDvsPortGroupManager(dv_switch)

    def test_create(self):
        self.assertTrue(self._vdpgm.create_port_group(PORTGROUP_NAME, NUM_PORT))

    def test_destroy(self):
        self.assertTrue(self._vdpgm.delete_port_group(PORTGROUP_NAME))


if __name__ == "__main__":
    unittest.main()
    