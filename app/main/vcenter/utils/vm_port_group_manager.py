# -*- coding:utf-8 -*-
from pyVmomi import vim
from pyVim.task import WaitForTask


class VMPortGroupManager:
    
    def __init__(self, host_system):
        self._host_system = host_system

    def create_port_group(self, vswitch_name, portgroup_name, vlan_id=0):
        """
        创建端口组
        """
        port_group = vim.host.PortGroup.Config()
        port_group.spec = vim.host.PortGroup.Specification()
        port_group.spec.vswitchName = vswitch_name
        port_group.spec.name = portgroup_name
        port_group.spec.vlanId = vlan_id
        port_group.spec.policy = vim.host.NetworkPolicy()   # TODO 优化配置

        try:
            self._host_system.configManager.networkSystem.AddPortGroup(
                portgrp=port_group.spec)
        except Exception as e:
            return False
        
        return True

    def delete_port_group(self, portgroup_name):
        """
        删除端口组
        """
        try:
            self._host_system.configManager.networkSystem.RemovePortGroup(
                pgName=portgroup_name)
        except Exception as e:
            return False
        
        return True
    

if __name__ == "__main__":
    import atexit
    from pyVim import connect
    from app.main.vcenter.control.utils import get_obj, connect_server
    hostname = '192.168.12.203'
    vswitch_name = 'vSwitch0'
    portgroup_name = 'test_group'
    # si, content, xx = get_connect(1)

    platform = {
        'ip': '192.168.12.205', 
        'name': 'administrator@vsphere.local', 
        'password': 'Aiya@2018', 
        'port': '443'
    }
    s = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
    atexit.register(connect.Disconnect, s)
    content = s.RetrieveContent()
    
    # container = content.viewManager.CreateContainerView(
    #     content.rootFolder, [vim.HostSystem], True)
    # for c in container.view:
    #     print c.name

    hs = get_obj(content, [vim.HostSystem], hostname)
    if hs:
        # print hs, dir(hs)
        # print hs.configManager, dir(hs.configManager)
        # print hs.configManager.networkSystem, dir(hs.configManager.networkSystem)
        # print vim.host.PortGroup.Config, dir(vim.host.PortGroup.Config())
        vpgm = VMPortGroupManager(hs)
        # vpgm.create_port_group(vswitch_name, portgroup_name)
        vpgm.delete_port_group(portgroup_name)
    else:
        print 'No Host System!!!'

    
# class VMDvsPortGroupManager:

#     def create_port_group(self):
#         """
#         1. 获取dswitch
#         2. 配置相关项目   目前考虑基本项
#         3. 调用dswitch的创建任务操作
#         4. 等待任务完成并且处理异常
#         """

#         config = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()

#         # Basic config
#         config.name = self.module.params['portgroup_name']
#         config.numPorts = self.module.params['num_ports']

#         try:
#             task = self.dv_switch.AddDVPortgroup_Task([config])
#             changed, result = wait_for_task(task)
#         except Exception as e:
#             print e
#             return False

#         return True

#     def delete_port_group(self):
#         """
#         1. 获取dswitch
#         2. 获取dswitch端口组
#         3. 调用dswitch的删除任务操作
#         4. 等待任务完成并且处理异常
#         """
#         try:
#             task = self.dvs_portgroup.Destroy_Task()
#             changed, result = wait_for_task(task)
#         except Exception as e:
#             print e
#             return False

#         return True
