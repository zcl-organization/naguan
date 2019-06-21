import unittest
from mock import Mock

from pyVmomi import vim
from app.main.base.control import cloud_platform
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_dvs import VMDvswitchManager
from app.main.vcenter.utils.vm_dvs import VMDvswitchHostManager

platforms = [
    {
        'ip': '192.168.78.205', 
        'name': 'administrator@vsphere.local', 
        'password': 'Aiya@2018', 
        'port': '443'
    },
]
folder_name = "test_network"

dvs_name = "test_name"
host_name = '192.168.78.59'

new_mtu = 2000
old_uplink_name = "AMD_Yes1"
new_uplink_name = "Intel_No 1"
switch_version = '6.6.0'
protocol = 'cdp'
operation = 'both' 

def find_folder(center, name):
    datacenter_obj = center.find_datacenter_by_name("Datacenter")
    content = center.connect
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.Folder], True)
    for folder in container.view:
        if folder.name == folder_name and \
            datacenter_obj.networkFolder.childType == folder.childType:
            return folder

    return None


def find_dvs(center, name):
    content = center.connect
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.DistributedVirtualSwitch], True)
    for dvs in container.view:
        if dvs.name == name:
            return dvs

    return None


class TestVMDvswitch(unittest.TestCase):
    def setUp(self):
        cloud_platform.platform_list = Mock(return_value=platforms)
        self._vcenter = VCenter(1)
        
        folder = find_folder(self._vcenter, folder_name)
        self._vmdvsm = VMDvswitchManager(self._vcenter.connect, folder)

    def test_01_create(self):
        kwargs = dict(
            switch_name=dvs_name,  # 端口组名称
            mtu=1500,    # mtu数据
            discovery_protocol="cdp",  # 发现协议配置类型  'cdp', 'lldp'
            discovery_operation="listen", # 发现协议配置操作  'both', 'advertise', 'listen'
            uplink_quantity=2,   # 上行链路组数量
            uplink_prefix="AMD_Yes",   # 上行链路组前缀名称
            switch_version='6.0.0',  # 交换机版本信息
        )
        self.assertTrue(self._vmdvsm.create(**kwargs))

    def test_02_update_mtu(self):
        self.assertTrue(self._vmdvsm.update_mtu(dvs_name, new_mtu))

    def test_03_update_link_protocol(self):
        self.assertTrue(self._vmdvsm.update_link_protocol(dvs_name, protocol, operation))

    def test_04_update_uplink_name(self):
        self.assertTrue(self._vmdvsm.update_uplink_name(dvs_name, old_uplink_name, new_uplink_name))

    def test_05_update_switch_version(self):
        self.assertTrue(self._vmdvsm.update_switch_version(dvs_name, switch_version))

    def test_06_host_add(self):
        dvs = find_dvs(self._vcenter, dvs_name)
        _vmdvshm = VMDvswitchHostManager(dvs)
        host = self._vcenter.find_hostsystem_by_name(host_name)
        self.assertTrue(_vmdvshm.add(host))

    def test_07_host_edit(self):
        dvs = find_dvs(self._vcenter, dvs_name)
        _vmdvshm = VMDvswitchHostManager(dvs)
        host = self._vcenter.find_hostsystem_by_name(host_name)
        self.assertTrue(_vmdvshm.edit(host))

    def test_08_host_remove(self):
        dvs = find_dvs(self._vcenter, dvs_name)
        _vmdvshm = VMDvswitchHostManager(dvs)
        host = self._vcenter.find_hostsystem_by_name(host_name)
        self.assertTrue(_vmdvshm.remove(host))

    def test_09_destroy(self):
        self.assertTrue(self._vmdvsm.destroy(dvs_name))

    
if __name__ == "__main__":
    unittest.main()
