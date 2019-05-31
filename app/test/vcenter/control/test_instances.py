import json
import unittest

from mock import Mock
from pyVmomi import vim
from pyVim.task import WaitForTask, WaitForTasks

from app.main.vcenter.control.instances import Instance
from manage import app
from app.main.base.control import cloud_platform
from app.main.vcenter.control import disks as disk_manage
from app.main.vcenter.control import network_devices as network_device_manage

create_info = {
    'new_cpu': '1',
    'new_memory': '512',
    'dc_id': 2,
    'ds_id': '', 
    'vm_name': 'unit_test1',
    'networks': '',
    'disks': '', 
    'image_id': ''
}
network_str = json.dumps([2,])
disk_str = json.dumps([{'type': 'thin', 'size': 16}, ])

snapshot_info = {
    'snapshot_name': 'unittest_snapshot_1',
    'description': 'unittest_description'
}

ip_info  = {
    'ip': '192.168.12.123',
    'subnet': '255.255.255.0',
    'gateway': '192.168.12.1',
    'dns': '8.8.8.8'
}
clone_name = "unit_test2"

class disk_info:
    label = 'Hard disk 1'

class network_info:
    label = 'Network adapter 1'


def get_obj(content, vimtype, name):
    obj = None
    # 创建连接视图获取相关类型
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True
    )
    # 查找对应项目
    for c in container.view:
        if c.name == name:
            obj = c
            break

    container.Destroy()
    return obj


class TestIntance(unittest.TestCase):

    def setUp(self):
        self.collect_data = {
            'platform_id': 1,
            # 'vm_uuid': '42016f82-0f85-9b36-1f90-d6580b264691'
        }
        platforms = [{'ip': '192.168.12.205', 'name': 'administrator@vsphere.local', 'password': 'Aiya@2018', 'port': '443'},]
        cloud_platform.platform_list = Mock(return_value=platforms)
        
        with app.test_request_context():
            self._uti = Instance(platform_id=self.collect_data['platform_id'])  # , uuid=self.collect_data['vm_uuid'])
            self._uti.update_vm_local = Mock(return_value=2)
    
    def tearDown(self):
        pass

    def test_010_boot(self):
        with app.test_request_context():
            self._uti.vm = None
            self._uti.boot(**create_info)
            self.assertIsNotNone(self._uti.vm)

    def test_011_start(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        self._uti.start()
        self.assertEqual(self._uti.vm.runtime.powerState, 'poweredOn')
        WaitForTask(self._uti.vm.PowerOff())

    def test_014_stop(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        if self._uti.vm.runtime.powerState == 'poweredOff':
            WaitForTask(self._uti.vm.PowerOn())
        
        self._uti.stop()
        self.assertEqual(self._uti.vm.runtime.powerState, 'poweredOff')

    def test_012_suspend(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        if self._uti.vm.runtime.powerState == 'poweredOff':
            WaitForTask(self._uti.vm.PowerOn())
        
        self._uti.suspend()
        self.assertEqual(self._uti.vm.runtime.powerState, 'suspended')
        WaitForTask(self._uti.vm.PowerOff())
 
    def test_013_restart(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)
        
        if self._uti.vm.runtime.powerState not in ['poweredOn',]:
            WaitForTask(self._uti.vm.PowerOn())

        self._uti.restart()
        self.assertEqual(self._uti.vm.runtime.powerState, 'poweredOn')
        WaitForTask(self._uti.vm.PowerOff())
    
    def test_015_update_vcpu(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        new_cpu = int(self._uti.vm.config.hardware.numCPU) + 1
        self._uti.update_vcpu(new_cpu, self._uti.vm.config.hardware.numCPU)
        self.assertEqual(int(self._uti.vm.config.hardware.numCPU), new_cpu)
    
    def test_016_update_vmemory(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        new_mem = int(self._uti.vm.config.hardware.memoryMB) + 512
        self._uti.update_vmemory(new_mem, self._uti.vm.config.hardware.memoryMB)
        self.assertEqual(int(self._uti.vm.config.hardware.memoryMB), new_mem)

    def test_017_add_network(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)
        
        old_network_info, new_network_info = None, None
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualE1000):
                old_network_info = item
        
        with app.test_request_context():
            self._uti.add_network(network_str)
        
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualE1000):
                new_network_info = item
            
        self.assertNotEqual(new_network_info, old_network_info)

    def test_018_del_network(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)
        network_device_manage.device_list_by_id = Mock(return_value=network_info())

        old_network_info, new_network_info = None, None
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualE1000):
                old_network_info = item
        
        with app.test_request_context():
            self._uti.del_network(network_str)
        
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualE1000):
                new_network_info = item
            
        self.assertNotEqual(new_network_info, old_network_info)

    def test_019_add_disk(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        old_disk_info, new_disk_info = None, None
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualDisk):
                old_disk_info = item
        
        with app.test_request_context():
            self._uti.add_disk(disk_str)
        
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualDisk):
                new_disk_info = item
            
        self.assertNotEqual(new_disk_info, old_disk_info)
    
    def test_020_delete_disk(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)
        disk_manage.get_disk_by_disk_id = Mock(return_value=disk_info())

        old_disk_info, new_disk_info = None, None
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualDisk):
                old_disk_info = item
        
        with app.test_request_context():
            self._uti.delete_disk([1,])
        
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualDisk):
                new_disk_info = item
            
        self.assertNotEqual(new_disk_info, old_disk_info)

    def test_021_add_image(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        old_image_info, new_image_info = None, None
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualIDEController):
                old_image_info = item
        
        with app.test_request_context():
            self._uti.add_image(1)
        
        for item in self._uti.vm.config.hardware.device:
            if isinstance(item, vim.vm.device.VirtualIDEController):
                new_image_info = item
            
        self.assertNotEqual(new_image_info, old_image_info)

    def test_022_add_snapshot(self):
        # self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name']))

        with app.test_request_context():
            self._uti.add_snapshot(**snapshot_info)
        
        self.assertEqual(self._uti.vm.snapshot.rootSnapshotList[0].name, snapshot_info["snapshot_name"])
        self.assertEqual(self._uti.vm.snapshot.rootSnapshotList[0].description, snapshot_info["description"])

    def test_023_revert_snapshot(self):
        # self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name']))

        new_mem = int(self._uti.vm.config.hardware.memoryMB) + 512
        self._uti.update_vmemory(new_mem, self._uti.vm.config.hardware.memoryMB)
        self.assertEqual(int(self._uti.vm.config.hardware.memoryMB), new_mem)
        
        revert_id = 1
        with app.test_request_context():
            self._uti.snapshot_revert(revert_id)
        
        self.assertEqual(int(self._uti.vm.config.hardware.memoryMB), new_mem-512)

    def test_024_delete_snapshot(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        delete_id = 1
        with app.test_request_context():
            self._uti.delete_snapshot(delete_id)
        
        self.assertIsNone(self._uti.vm.snapshot)

    def test_025_clone(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        with app.test_request_context():
            self._uti.clone(clone_name, 1)
        
        dd = get_obj(self._uti.content, [vim.VirtualMachine], clone_name)
        self.assertEqual(dd.summary.config.name, clone_name)
        WaitForTask(dd.Destroy())

    def test_026_cold_migrate(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)

        old_vm_name = self._uti.vm.summary.config.name
        old_instance_uuid = self._uti.vm.summary.config.instanceUuid

        with app.test_request_context():
            self._uti.cold_migrate('192.168.12.203', 1)
        
        dd = get_obj(self._uti.content, [vim.VirtualMachine], old_vm_name)
        self.assertEqual(dd.summary.config.name, old_vm_name)
        self.assertNotEqual(dd.summary.config.instanceUuid, old_instance_uuid)

    # def test_027_ip_assignment(self):
    #     self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
    #     self._uti._set_vm(self._uti.vm)
    #     # import time
        
    #     # self._uti.start()
    #     # for item in range(5):
    #     #     print self._uti.vm.summary
    #     #     print "---- {} ----".format(item)
    #     #     time.sleep(10)
    #     with app.test_request_context():
    #         self._uti.ip_assignment(**ip_info)
    #     # self._uti.ip_assignment(**ip_info)
    #     # self._uti._vm_base_manager.start()
    #     print self._uti.vm.config
    #     print self._uti.vm.summary

    def test_100_delete(self):
        self._uti.vm = get_obj(self._uti.content, [vim.VirtualMachine], create_info['vm_name'])
        self._uti._set_vm(self._uti.vm)
        self._uti.delete()
    


if __name__ == "__main__":
    unittest.main()
